#!/usr/bin/env python

from util import *
import json


# public api
def get_symbols():
    url = HTTP_URL + "/open/api/common/symbols"
    return http_get_request(url, None)


def get_market_price():
    url = HTTP_URL + "/open/api/market"
    return http_get_request(url, None)


def get_kline(symbol, period, size=150):
    """
    :param symbol:
    :param period: ["1min","5min","15min","30min","60min","2hour","4hour","6hour","12hour","1day","1week","1month"]
    :param size: [1,2000] default 150
    :return:
    """
    url = HTTP_URL + "/open/api/get_records"
    params = {"symbol": symbol,
              "period": period,
              "size": size}
    return http_get_request(url, params)


def get_market_depth(symbol, type="step0"):
    """
    :param symbol:
    :param type: ["step0", "step1", "step2"]
    :return:
    """
    url = HTTP_URL + "/open/api/market_dept"
    params = {"symbol": symbol,
              "type": type}
    return http_get_request(url, params)


def get_market_ticker(symbol):
    """
    :param symbol:
    :return:
    """
    url = HTTP_URL + "/open/api/get_ticker"
    params = {"symbol": symbol}
    return http_get_request(url, params)


def get_market_trades(symbol, size=100):
    """
    :param symbol:
    :param size: [1,200] default 100
    :return:
    """
    url = HTTP_URL + "/open/api/get_trades"
    params = {"symbol": symbol,
              "size": size}
    return http_get_request(url, params)


# user trade api
def create_order(symbol, side, type, volume, price):
    """
    :param side: 'BUY' or 'SELL'
    :param type: 1: limit order, 2: market order
    :param volume: --- type=1(limit), the quantity to buy or sell
                   |__ type=2(market), --- side='BUY',  the amount you cost
                                       |__ side='SELL', the quantity to sell
    :param price:  --- type=1(limit), the worst price that can be accepted
                   |__ don't need this param, means nothing
    :param symbol: for example: 'btcusdt'
    :return:
    """
    url = HTTP_URL + "/open/api/create_order"
    params = {"side": side,
              "type": type,
              "volume": volume,
              "price": price,
              "symbol": symbol}
    return api_key_post(url, params)


def cancel_order(symbol, order_id):
    """
    :param symbol:
    :param order_id:
    :return:
    """
    url = HTTP_URL + "/open/api/cancel_order"
    params = {"symbol": symbol,
              "order_id": order_id}
    return api_key_post(url, params)


def get_all_order(symbol, page=1, page_size=20):
    """
    :param symbol:
    :param page:
    :param page_size:
    :return:
    """
    url = HTTP_URL + "/open/api/all_order"
    params = {"symbol": symbol,
              "pageSize": page_size,
              "page": page}
    return api_key_get(url, params)


def get_new_order(symbol, page=1, page_size=20):
    """
    :param symbol:
    :param page:
    :param page_size:
    :return:
    """
    url = HTTP_URL + "/open/api/new_order"
    params = {"symbol": symbol,
              "pageSize": page_size,
              "page": page}
    return api_key_get(url, params)


def get_all_trade(symbol, page=1, page_size=20):
    """
    :param symbol:
    :param page:
    :param page_size:
    :return:
    """
    url = HTTP_URL + "/open/api/all_trade"
    params = {"symbol": symbol,
              "pageSize": page_size,
              "page": page}
    return api_key_get(url, params)


def get_order_detail(symbol, order_id):
    """
    :param symbol:
    :return:
    """
    url = HTTP_URL + "/open/api/order_info"
    params = {"symbol": symbol,
              "order_id": order_id}
    return api_key_get(url, params)


def get_account():
    """
    :return:
    """
    url = HTTP_URL + "/open/api/user/account"
    return api_key_get(url, {})


if __name__ == "__main__":
    print json.dumps(get_symbols())
    print json.dumps(get_market_price())

    ret = create_order("eosusdt", "SELL", 1, 0.1, 10)
    print ret
    order_id = ret.get("data").get("order_id")
    print cancel_order("eosusdt", order_id)
    print json.dumps(get_all_order("eosusdt", 1, 10))
    print json.dumps(get_new_order("eosusdt", 1, 10))
    print json.dumps(get_all_trade("eosusdt", 1, 10))
    print json.dumps(get_kline("eosusdt", "1min", 100))
    print json.dumps(get_market_ticker("eosusdt"))
    print json.dumps(get_market_trades("eosusdt", 100))
    print json.dumps(get_market_depth("eosusdt", "step0"))
    print json.dumps(get_order_detail("eosusdt", order_id))
    print json.dumps(get_account())
