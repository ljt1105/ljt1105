import os
import shutil



# if __name__ == "__main__":
def copy_files():
    open_position = r"Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test/잔고보고서"
    new_transaction = r"Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test/신규거래"
    unwind_transaction = r"Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test/청산거래"
    mid_settle_transaction = r"Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test/정산거래"

    data_reservoir = r"Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test/Data Reservoir"

    open_position_files = os.listdir(open_position)
    new_transaction_files = os.listdir(new_transaction)
    unwind_transaction_files = os.listdir(unwind_transaction)
    mid_settle_transaction_files = os.listdir(mid_settle_transaction)

    if not os.path.exists(data_reservoir):
        os.mkdir(data_reservoir)


    for file in open_position_files:
        if 'xlsx' in file:
            shutil.copy(open_position+"/"+file, data_reservoir+"/"+file)
    print("Open position file copy completed")

    for file in new_transaction_files:
        if 'xlsx' in file:
            shutil.copy(new_transaction+"/"+file, data_reservoir+"/"+file)
    print("New trasaction file copy completed")

    for file in unwind_transaction_files:
        if 'xlsx' in file:
            shutil.copy(unwind_transaction+"/"+file, data_reservoir+"/"+file)
    print("Unwind transaction file copy completed")

    for file in mid_settle_transaction_files:
        if 'xlsx' in file:
            shutil.copy(mid_settle_transaction+"/"+file, data_reservoir+"/"+file)
    print("Mid settle transaction file copy completed")