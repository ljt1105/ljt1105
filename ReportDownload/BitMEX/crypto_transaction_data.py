from datetime import timezone, datetime

from bitmex import bitmex

# 세션 연결
api_key = "Oh78RlN2sIGUYYN05i595jw2"
api_secret = "-HwtPs33XepJndRtkaESiJK6o9MIcNm7Lw0wlGPEVRGChj79"
test = True
bitmex_session = bitmex(test=test, api_key=api_key, api_secret=api_secret)

# 파라미터설정
"""
비트맥스에서 사용하는 통화 단위
"BTC": "XBt", "USDT": "USDt", "ETH": "Gwei", "SOL": "LAMp",
"""
currency = "all"
start_datetime = datetime(2025, 1, 1, tzinfo=timezone.utc)
end_datetime = datetime.now(tz=timezone.utc)
result = []
start = 0
done = False

# 조회 시 start를 증가 시키며 반복적으로 증가 시킵니다.
while not done and (
    wallet_history_dicts := bitmex_session.User.User_getWalletHistory(
        count=10_000, start=start, currency=currency
    )
    .response()
    .result
):
    # 해당 api가 기간별 조회가 되지 않기 때문에, 결과값을 조회 후 해당 기간에 포함되는 값들만 포함 시킵니다.
    for wallet in wallet_history_dicts:
        timestamp = wallet["timestamp"]
        if timestamp < start_datetime:
            done = True
            break
        if timestamp > end_datetime:
            start += 1
            continue
        result.append(wallet)
    start += len(result)
result.sort(key=lambda r: r["timestamp"])
for r in result:
    print(r)