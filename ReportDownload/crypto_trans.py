import os
import pandas as pd
import shutil
import openpyxl
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path
import win32com.client
import zipfile
import datetime
import ccxt

def extract_attachments(output_dir, attachments):
    for attachment in attachments:
        attachment_name = str(attachment)
        attachment_path = output_dir / attachment_name

        if attachment_name.lower().endswith('.zip'):
            # 첨부 파일이 .zip 형식인 경우 압축을 풉니다.
            with zipfile.ZipFile(attachment_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            # os.remove(attachment_path)  # 압축 파일은 삭제할 수도 있습니다.
        else:
            # .zip이 아닌 경우 무시
            continue

def cryptoTransactionHistory_download():
    output_dir = Path("Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("Crypto Transaction")
    messages = inbox.Items

    for message in messages:
        if message.Unread:

            attachments = message.Attachments

            target_folder = output_dir
            target_folder.mkdir(parents=True, exist_ok=True)

            for attachment in attachments:
                attachment.SaveAsFile(target_folder / str(attachment))
                
                if message.Unread:
                    message.Unread = False

            extract_attachments(output_dir, attachments)

    print("Crypto Transaction History download complete")



def rpt_move(pre_source_dir, pre_dest_dir, rpt_keyword):
    # 특정 키워드를 포함하고 확장자가 .csv인 파일 복사
    try:
        files_moved = 0
        for file_name in os.listdir(pre_source_dir):
            # 파일명에 키워드 포함 여부와 확장자가 ".csv"인지 확인
            if rpt_keyword in file_name and file_name.endswith(".csv"):
                source_file_path = os.path.join(pre_source_dir, file_name)
                if os.path.isfile(source_file_path):  # 파일인지 확인
                    shutil.move(source_file_path, pre_dest_dir)
                    files_moved += 1
                    print(f"'{file_name}' 파일을 이동됐습니다.")
        
        if files_moved == 0:
            print("이동시킬 파일이 없습니다.")
        else:
            print(f"총 {files_moved}개의 파일이 성공적으로 이동되었습니다.")
    except Exception as e:
        print(f"파일 이동 중 오류가 발생했습니다: {e}")

def combine_transaction_data(data_path, save_path, output_filename, close_price_data):
    all_data = []

    for filename in os.listdir(data_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_path, filename)
            data = pd.read_csv(file_path)

            if 'transactTime' in data.columns:
                data['Date'] = data['transactTime'].str[:10]

            all_data.append(data)

    combined_data = pd.concat(all_data, ignore_index=True)
    combined_data = combined_data.drop_duplicates()

    # setCurrency 값 수정 (병합 조건 일치)
    combined_data['settlCurrency'] = combined_data['settlCurrency'].replace({'XBt': 'XBTUSD', 'USDT': 'USDT/USD'})

    # 종가 데이터 병합
    combined_data = combined_data.merge(
        close_price_data,
        how='left',
        left_on=['Date', 'settlCurrency'],
        right_on=['Date', 'Symbol']
    ).rename(columns={'Close Price': 'Close Price'})

    # USD 실현 손익 계산
    combined_data['USD_realisedPnL'] = combined_data.apply(
        lambda row: row['realisedPnl'] * row['Close Price'] / 10**8 if row['settlCurrency'] == 'XBTUSD'
        else row['realisedPnl'] / 10**6 if row['settlCurrency'] == 'USDt'
        # else row['realisedPnl'] * row['Close Price'] if row['settlCurrency'] == 'USDt'
        else row['realisedPnl'],
        axis=1
    )

    output_path = os.path.join(save_path, output_filename + '.xlsx')
    combined_data.to_excel(output_path, index=False)

    print(f"{output_filename} has been combined and saved to {save_path}")

def get_close_prices_ccxt(exchange_name, symbols, start_date, end_date):
    """
    Get daily close prices for multiple symbols using CCXT from a specified exchange.
    """
    exchange = getattr(ccxt, exchange_name)()  # Initialize exchange
    timeframe = '1d'  # Daily data
    results = []

    for symbol in symbols:
        since = exchange.parse8601(f"{start_date}T00:00:00Z")  # Start date in ISO format
        ohlcv = []
        
        # Fetch historical OHLCV (Open, High, Low, Close, Volume) data
        while since < exchange.parse8601(f"{end_date}T00:00:00Z"):
            candles = exchange.fetch_ohlcv(symbol, timeframe, since)
            if not candles:
                break
            ohlcv.extend(candles)
            since = candles[-1][0] + 24 * 60 * 60 * 1000  # Move to the next day

        # Convert OHLCV data to DataFrame
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['Date'] = pd.to_datetime(data['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
        data['Symbol'] = symbol  # Add symbol column for distinction
        results.append(data[['Date', 'Symbol', 'close']])

    # Combine results for all symbols
    combined_data = pd.concat(results, ignore_index=True)
    return combined_data.rename(columns={'close': 'Close Price'})

def volume_data_combine():
    # 병합할 CSV 파일들이 저장된 폴더 경로
    folder_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/liquidity"  # 수정 필요
    output_file = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/merged_volume.xlsx"

    # 병합 결과를 저장할 빈 데이터프레임 생성
    merged_data = pd.DataFrame()

    # 폴더 내 모든 CSV 파일 처리
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):  # csv 파일만 처리
            file_path = os.path.join(folder_path, file)
            try:
                # CSV 파일 읽기
                df = pd.read_csv(file_path)
                
                # 필요한 열만 선택
                filtered_df = df[['Report Contract', 'Report Period', 'Total Volume in USD']].copy()

                # Report Period 열의 값을 날짜 형식으로 변환
                filtered_df['Report Period'] = pd.to_datetime(
                    filtered_df['Report Period'].apply(lambda x: ' '.join(str(x).split()[:3])),  # 처음 세 단어만 추출
                    format='%d %b %Y'  # 날짜 형식 지정 ('10 Nov 2024'와 같은 형식)
                ).dt.strftime('%Y-%m-%d')  # 최종적으로 'YYYY-MM-DD' 형식으로 변환

                # Total Volume in USD 열에서 'USD ' 및 쉼표 제거 후 숫자로 변환
                filtered_df['Total Volume in USD'] = filtered_df['Total Volume in USD'].str.replace(
                    'USD ', '', regex=False
                ).str.replace(',', '').replace('', '0')  # 쉼표 제거 및 빈 값은 0으로 대체
                filtered_df['Total Volume in USD'] = filtered_df['Total Volume in USD'].astype(float)

                # 병합 데이터프레임에 추가
                merged_data = pd.concat([merged_data, filtered_df], ignore_index=True)
            except KeyError as e:
                print(f"Missing columns in {file}: {e}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    # 병합 결과 저장
    merged_data.to_excel(output_file, index=False)
    print(f"Merged file saved as {output_file}")

def main():

    # cryptoTransactionHistory_download()

    # crt_accounts_source = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record"

    # strat_1356824_wallet = "1356824_wallet"
    # strat_1356824_trade = "1356824_trade"
    # crt_1356824_wal_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/wallet/1356824"
    # crt_1356824_tr_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/1356824"
    # rpt_move(crt_accounts_source, crt_1356824_wal_dest, strat_1356824_wallet)
    # rpt_move(crt_accounts_source, crt_1356824_tr_dest, strat_1356824_trade)

    # strat_238210_wallet = "238210_wallet"
    # strat_238210_trade = "238210_trade"
    # crt_238210_wal_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/wallet/238210"
    # crt_238210_tr_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/238210"
    # rpt_move(crt_accounts_source, crt_238210_wal_dest, strat_238210_wallet)
    # rpt_move(crt_accounts_source, crt_238210_tr_dest, strat_238210_trade)

    # strat_476727_wallet = "476727_wallet"
    # strat_476727_trade = "476727_trade"
    # crt_476727_wal_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/wallet/476727"
    # crt_476727_tr_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/476727"
    # rpt_move(crt_accounts_source, crt_476727_wal_dest, strat_476727_wallet)
    # rpt_move(crt_accounts_source, crt_476727_tr_dest, strat_476727_trade)

    # strat_1223695_wallet = "1223695_wallet"
    # strat_1223695_trade = "1223695_trade"
    # crt_1223695_wal_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/wallet/1223695"
    # crt_1223695_tr_dest = r"Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/1223695"
    # rpt_move(crt_accounts_source, crt_1223695_wal_dest, strat_1223695_wallet)
    # rpt_move(crt_accounts_source, crt_1223695_tr_dest, strat_1223695_trade)

    # current_date = datetime.datetime.now()
    # td = current_date.strftime("%Y-%m-%d")

    # start_date = '2024-08-01'
    # end_date = td
    # symbols = ['XBTUSD']
    # btc_close_data = get_close_prices_ccxt('bitmex', symbols, start_date, end_date)

    # save_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record"
    # dir238210_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/238210"
    # filename_238210 = "238210_rawdata_"
    # dir476727_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/476727"
    # filename_476727 = "476727_rawdata_"
    # dir1356824_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/1356824"
    # filename_1356824 = "1356824_rawdata_"
    # dir1223695_path = "Z:/02.펀드/020. Crypto_Fund/03. Daily Trade Record/trade/1223695"
    # filename_1223695 = "1223695_rawdata_"
    # combine_transaction_data(dir238210_path, save_path, filename_238210, close_price_data=btc_close_data)
    # combine_transaction_data(dir476727_path, save_path, filename_476727, close_price_data=btc_close_data)
    # combine_transaction_data(dir1356824_path, save_path, filename_1356824, close_price_data=btc_close_data)
    # combine_transaction_data(dir1223695_path, save_path, filename_1223695, close_price_data=btc_close_data)

    volume_data_combine()


if __name__ == "__main__":
    main()