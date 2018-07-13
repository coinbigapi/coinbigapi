import time
import base64
import hashlib
import requests
import json
import random
import urllib
import copy
import operator
import logging, pdb

from enum import Enum, unique


@unique
class StatusErrorCode(Enum):
    """docstring for StatusCode"""
    balance_insufficient = -2
    


class CoinBig():
    def __init__(self):
        self.base_url = 'https://www.coinbig.com/api/publics/v1'
        self.time = 3
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.timeout = 10

    def auth(self, key , secret):
        self.apiKey = key 
        self.secret = secret

    def handler_error_if_needed(self, json):
        status = json['code']
        if status == StatusErrorCode.balance_insufficient.value:
            raise Exception(status)
        


    def sign(self, params):
        params["time"] = int(round(time.time() * 1000))
        _params = copy.copy(params)
        sort_params = sorted(_params.items(), key=operator.itemgetter(0))
        sort_params = dict(sort_params)
        sort_params['secret_key'] = self.secret
        string = urllib.parse.urlencode(sort_params)
        # _sign1 = hashlib.md5(bytes('abc'.encode('utf-8'))).hexdigest().upper()
        _sign = hashlib.md5(bytes(string.encode('utf-8'))).hexdigest().upper()
        params['sign'] = _sign
        return params

    def public_request(self, method, api_url, **payload):
        shouldRepeat = True
        while shouldRepeat:
            try:
                r_url = self.base_url + api_url
                if method == 'POST':
                    r = requests.request(method, r_url, json=payload, timeout = self.timeout, headers = self.headers)
                else:
                    r = requests.request(method, r_url, params=payload, timeout = self.timeout, headers = self.headers)
                logging.info(r)
            except Exception as err:
                logging.info('%s'%(err))
                time.sleep(self.time)
                
            else:
                r.raise_for_status()

                if r.status_code == 200 and r.json()['code'] == 0:
                    logging.info('%s'%(r.json()))
                    return r.json()
                else:
                    logging.info('%s'%(r.json()))
                    self.handler_error_if_needed(r.json())
                    time.sleep(self.time)
                    
            

    def signed_request(self, method, api_url, data = {}):
        new_data = copy.copy(data)
        new_data['apikey'] = self.apiKey
        # new_data['time'] = str(int(time.time() * 1000))
        print('new_data', new_data)
        try:
            url = self.base_url + api_url
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            r = requests.request('POST', url, data = self.sign(new_data), headers = headers)
            
        except Exception as err:
            logging.info('err %s'%(err))
            time.sleep(self.time)
            
        else:
            r.raise_for_status()
            if r.status_code == 200 and r.json()['code'] == 0:
                self.handler_error_if_needed(r.json())
                logging.info('success %s'%(r.json()))
                return r.json()
            else:
                logging.info('not 200 %s'%(r.json()))
                self.handler_error_if_needed(r.json())
                time.sleep(self.time)
                


    def list_symbol_precision(self):
        return self.public_request('GET', '/listSymbolPrecision')


    


    # # 获取所有订单信息
    # def orders_info(self,symbol,trade_type,nums):
    #     url = self.url +'/orders_info'
    #     params = {'apikey':self.apiKey,'symbol':trade_type,'size':nums,'type':3}
    #     data = self.sign(params)
    #     res = requests.post(url,data=data)
    #     return res.json()


    # 用户信息
    def userinfo(self):
        return self.signed_request('POST', '/userinfo')

    def cancel_order(self, order_id):
        params = {'order_id': order_id}
        return self.signed_request('POST', '/cancel_order', params)

    def ticker(self, symbol):
        return self.public_request('GET', '/ticker', symbol = symbol)

    #买卖类型: 限价单(buy/sell) 市价单(buy_market/sell_market)
    def trade(self, symbol, trade_type, price, amount):
        params = {
            'type': trade_type,
            'price': price,
            'amount': amount,
            'symbol': symbol
        }
        return self.signed_request('POST', '/trade', params)








