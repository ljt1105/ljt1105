import datetime
import requests
import input_database
import pandas as pd
import uuid
import time
# import constants
from datetime import datetime
from operator import itemgetter
# from stock.common_function import get_uuid_list_through_filter, get_uuid_use_string_account



def period_pnl_details(_from: str, _to: str):
    performance_url = 'http://43.202.36.216:13070/performance/accounts/'
    macro_list = get_uuid_list_through_filter("macro-stock") + get_uuid_list_through_filter("macro-futures")
    ipo_list = get_uuid_list_through_filter("venture-1-ipo-ipo") + get_uuid_list_through_filter("venture-1-ipo-new")\
               + get_uuid_list_through_filter("multi-1-ipo-") + get_uuid_list_through_filter("ipo-1-ipo-")
    block_list = get_uuid_list_through_filter("block-stock") + get_uuid_list_through_filter("block-futures")
    event_list = get_uuid_list_through_filter("event-stock") + get_uuid_list_through_filter("event-futures")
    post_list = get_uuid_list_through_filter("post-stock") + get_uuid_list_through_filter("post-futures")
    account_list_proper = [
                              input_database.account_nh_futures['accountId'],
                              input_database.account_nh["accountId"],
                              input_database.account_samsung_trs["accountId"],
                              input_database.account_samsung_cfd["accountId"],
                              input_database.account_kiwoom["accountId"],
                              input_database.account_kiwoom_futures["accountId"],
                              input_database.account_proper_ipo['accountId']
                          ]
    account_list_bond = get_uuid_list_through_filter("bond-1-")
    account_list_ipo = get_uuid_list_through_filter("ipo-1-")
    account_list_ipo2 = get_uuid_list_through_filter("ipo-2-")
    account_list_focus = get_uuid_list_through_filter("ipo-focus-")
    account_list_alpha = get_uuid_list_through_filter("ipo-alpha-")
    account_list_kv = get_uuid_list_through_filter("venture-1-")
    account_list_multi = get_uuid_list_through_filter("multi-1-")
    account_list_bvi_ent = get_uuid_list_through_filter("ent-stock")
    account_list_bnk_ent = get_uuid_list_through_filter("et-db")
    account_list_ipo_block = get_uuid_list_through_filter("ipo-block")
    account_list_alpha = get_uuid_list_through_filter("alpha-ipo-stock")
    account_list_bvi_proper_stock = ["5a4e121d-0a90-4bd9-afe2-3bf831439e97"]
    account_list_bvi_proper_futures = ["87ca1269-1df9-450c-af7e-823083c5c06a"]
    account_list_hk_ipo = ["916d47d3-2021-47cb-bfd5-ff62cd2818fb", "1ef4080a-c526-4495-9dd7-12ac974c6b85"]
    account_list_maven = ['157280dd-72ce-4a4a-899b-57f293640f94']
    # all_fund_account = account_list_multi
    # all_fund_account = account_list_bond + account_list_ipo + account_list_ipo2 + account_list_focus + account_list_kv +\
    #                    account_list_multi + account_list_alpha + account_list_ipo_block
    # all_fund_account = account_list_ipo2 + account_list_bond + account_list_focus + account_list_alpha
    all_fund_account = account_list_bond + account_list_ipo + account_list_ipo2 + account_list_focus + account_list_alpha + account_list_kv +\
                       account_list_multi + account_list_bvi_ent + account_list_bnk_ent + account_list_proper + \
                       account_list_bvi_proper_stock + account_list_bvi_proper_futures + account_list_hk_ipo + account_list_maven
    sum_list = list()
    for _account in all_fund_account:
        input_ecm = {
            "accountId": _account,
            "from": _from,
            "to": _to
        }
        try:
            positions_list = requests.get(url=performance_url + str(_account), params=input_ecm).json()['body']
            sum_list += positions_list['positionPerformances']
        except KeyError:
            continue
    cumulative_list = list()
    for _page in sum_list:
        try:
            _member, _ticker, _asset_type, _stock_name, _listing_date, _order_list = position_id_info(_page['positionId'])
        except TypeError:
            continue
        perform_dict = dict()
        if _page['accountId'] in macro_list:
            perform_dict['strategy'] = 'Macro'
        elif _page['accountId'] in ipo_list:
            perform_dict['strategy'] = 'IPO'
        elif _page['accountId'] in event_list:
            perform_dict['strategy'] = 'event'
        elif _page['accountId'] in block_list:
            perform_dict['strategy'] = 'block'
        elif _page['accountId'] in post_list:
            perform_dict['strategy'] = 'post'
        else:
            perform_dict['strategy'] = 'LS'
        if _page['accountId'] in account_list_proper:
            perform_dict['fund'] = 'proper'
        if _page['accountId'] in account_list_ipo:
            perform_dict['fund'] = 'ipo'
        elif _page['accountId'] in account_list_kv:
            perform_dict['fund'] = 'kv'
        elif _page['accountId'] in account_list_multi:
            perform_dict['fund'] = 'multi'
        elif _page['accountId'] in account_list_ipo2:
            perform_dict['fund'] = 'ipo2'
        elif _page['accountId'] in account_list_focus:
            perform_dict['fund'] = 'focus'
        elif _page['accountId'] in account_list_alpha:
            perform_dict['fund'] = 'alpha'
        elif _page['accountId'] in account_list_bond:
            perform_dict['fund'] = 'bond'
        elif _page['accountId'] in account_list_bvi_ent:
            perform_dict['fund'] = 'bvi'
        elif _page['accountId'] in account_list_bnk_ent:
            perform_dict['fund'] = 'bnk'
        elif _page['accountId'] in account_list_hk_ipo:
            perform_dict['fund'] = 'hk'
        elif _page['accountId'] in account_list_bvi_proper_stock or _page['accountId'] in account_list_bvi_proper_futures:
            _page['fund'] = 'bprop'
        elif _page['accountId'] in account_list_hk_ipo:
            _page['fund'] = "hk"
        elif _page['accountId'] in account_list_maven:
            _page['fund'] = "maven"
        elif _page['accountId'] in account_list_alpha:
            _page['fund'] = "alpha"
        perform_dict['accountId'] = _page['accountId']
        perform_dict['member'] = _member
        perform_dict['position_id'] = _page['positionId']
        perform_dict['ticker'] = _ticker
        perform_dict['stockName'] = _stock_name
        perform_dict['exposure'] = find_final_delta_by_position_id(_page['positionId'])
        perform_dict['grossbuy'] = _page['grossValueBuy']
        perform_dict['grosssell'] = _page['grossValueSell']
        perform_dict['gross_expo'] = abs(_page['grossValueBuy'] + _page['grossValueSell']) - abs(_page['realizedPnl'])
        perform_dict['market'] = _asset_type
        perform_dict['direction'] = find_direction_by_position_id(_page['positionId'])
        perform_dict['capital'] = check_stock_capitalization(_ticker)
        perform_dict['openDateTime'] = _order_list
        perform_dict['quantity'] = _page['quantity']
        perform_dict['unrealizedPnl'] = _page['unrealizedPnl']
        perform_dict['realizedPnl'] = _page['realizedPnl']
        perform_dict['comm'] = _page['commissionFee']
        perform_dict['stamp'] = _page['stampDuty']
        perform_dict['cumulative_pnl'] = _page['cumulativePnl'] + perform_dict['comm'] + perform_dict['stamp']
        if perform_dict['ticker'] == "252670":
            perform_dict['direction'] = "S"
            perform_dict['exposure'] = perform_dict['exposure'] * 2
        elif perform_dict['ticker'] == "251340":
            perform_dict['direction'] = "S"
        cumulative_list.append(perform_dict)
    fund_pnl_data = pd.DataFrame(cumulative_list)
    fund_pnl_data.to_excel(f'{_from}.xlsx', index=False, sheet_name="raw_data")
    # 저장 경로 출력
    print(f"Excel file saved at: {_from}")
    return fund_pnl_data



def position_id_info(_position_id):
    positions_id = {
        'positionId': _position_id
    }
    position_info = \
        requests.get(url=input_database.url_positions_information + str(_position_id), params=positions_id).json()[
            'body']
    if position_info is None:
        return None
    elif position_info['memberId'] == input_database.member_hj['memberId']:
        _member = 'hj'
    elif position_info['memberId'] == input_database.member_jr['memberId']:
        _member = 'jr'
    elif position_info['memberId'] == input_database.member_yc['memberId']:
        _member = 'yc'
    elif position_info['memberId'] == input_database.member_dk['memberId']:
        _member = 'dk'
    elif position_info['memberId'] == input_database.member_jj['memberId']:
        _member = 'jj'
    else:
        _member = 'pm'
    _ticker = position_info['ticker']
    _asset_type = position_info['assetType']
    get_name = requests.get(url=input_database.url_stock_ticker + str(_ticker), params={"ticker": _ticker}).json()[
        'body']
    _stock_name = get_name['name']
    _listing_date = get_name['listingDate']
    position_order_info = requests.get(
        url=input_database.url_position_basic + str(_position_id), params=positions_id
    ).json()['body']['orders']
    try:
        order_date = order_split(position_order_info)
    except KeyError:
        order_date = []

    return _member, _ticker, _asset_type, _stock_name, _listing_date, order_date


def find_final_delta_by_position_id(position_id):
    payload = {"positionId": position_id}
    response = requests.get(input_database.url_position_basic + str(position_id), params=payload).json()
    order_info = response["body"]["orders"]
    direction = find_direction_by_position_id(position_id)
    list_len = len(order_info)
    position_exposure = 0
    if list_len == 1:
        position_exposure = abs(order_info[0]["notionalValue"])
    else:
        for i in range(0, list_len - 1):
            if (order_info[i]['notionalValue'] * order_info[i + 1]['notionalValue']) > 0:
                position_exposure += order_info[i]['notionalValue']
            else:
                position_exposure += order_info[i]['notionalValue']
                break
    return abs(position_exposure)

def find_direction_by_position_id(_position_id):
    position_id = {
        "positionId": _position_id
    }
    position_order_info = requests.get(
        url=input_database.url_position_basic + str(_position_id), params=position_id
    ).json()['body']['orders']
    sorted_orders = sorted(position_order_info, key=itemgetter("orderDateTime"))
    if sorted_orders[0]['quantity'] < 0:
        return "S"
    else:
        return "L"

def check_stock_capitalization(_ticker):
    stock_info = {
        "ticker": f'{_ticker}'
    }
    stock_request = requests.get(
        url=input_database.url_list_new + str(_ticker), params=stock_info
    ).json()['body']
    if stock_request['marketCapitalization'] <= 5000000000000:
        return "Small"
    else:
        return "Large"


def get_uuid_list_through_filter(_filter):
    uuid_list = list()
    filter_list = [item for item in input_database.account_list if f'{_filter}' in item]
    for _account in filter_list:
        input_alias = {
            "accountId": _account
        }
        alias_to_uuid = requests.get(url=input_database.url_search, params=input_alias).json()['body']["accountId"]
        uuid_list.append(alias_to_uuid)
    return uuid_list

def order_split(_order_list):
    date_list = list()
    for _order in _order_list:
        date_list.append(str(_order['orderDateTime'])[0:10])
    return date_list


period_pnl_details("2024-01-01","2024-06-30")