import time
import base64
import hashlib
import requests
import json
import random
import copy
import operator
from urllib.request import urlopen, Request
import json
import urllib


class CoinBigHelper():
    def __init__(self,url,apikey,secretkey):
        self.url = url
        self.apiKey = apikey
        self.secret = secretkey

    # def __init__(self, apiKey='', secret=''):
    #     self.url = 'http://www.3k2k.com:81/api/publics/v1'
    #     self.apiKey = apiKey
    #     self.secret = secret

    def httpGet(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        request = Request(url=url, headers=headers)
        content = urlopen(request, timeout=15).read()
        content = content.decode('utf-8')
        json_data = json.loads(content)
        return json_data

    def httpPost(self,url, params):
        url = 'https://' + url
        temp_params = urllib.parse.urlencode(params)
        data = bytes(temp_params, encoding='utf8')
        print(data)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        request = Request(url=url, data=data, headers=headers)
        content = urlopen(request, timeout=30).read()
        print(content)
        json_data = json.loads(content)
        return json_data

    def sign(self, params):
        _params = copy.copy(params)
        sort_params = sorted(_params.items(), key=operator.itemgetter(0))
        sort_params = dict(sort_params)
        sort_params['secret_key'] = self.secret
        string = urllib.parse.urlencode(sort_params)
        # _sign1 = hashlib.md5(bytes('abc'.encode('utf-8'))).hexdigest().upper()
        _sign = hashlib.md5(bytes(string.encode('utf-8'))).hexdigest().upper()
        params['sign'] = _sign
        return params

    # 获取用户的提现/充值记录
    def account_records(self, ):
        url = self.url + '/account_records'
        params = {'apikey': self.apiKey, 'shortName': 'btc_usdt', 'status': 0, 'recordType': 0}

        data = self.sign(params)
        #res = requests.post(url, data=data)
        res = self.httpPost(url,data=data)
        return res.json()

    # 获取所有订单信息
    def orders_info(self, symbol,  size,type):
        url = self.url + '/api/publics/v1/orders_info'
        params = {'apikey': self.apiKey, 'symbol': symbol, 'size': size, 'type': type}
        data = self.sign(params)
        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()

    # 用户信息
    def userinfo(self):
        url = self.url + '/api/publics/v1/userinfo'

        params = {'apikey': self.apiKey}
        data = self.sign(params)
        # res = requests.post(url, data=data)
        # thejson = res.json()
        res = self.httpPost(url, data=data)
        thejson = res.json()
        return thejson

    # 下订单
    def trade(self, type, price, amount,symbol):
        '''
        type    String 买卖类型: 限价单(buy/sell) 市价单(buy_market/sell_market)
        price   double  否   下单价格 [限价买单(必填)
        amount  double  否   交易数量 [限价卖单（必填)
        '''
        url = self.url + '/api/publics/v1/trade'
        params = {'amount': amount,'apikey': self.apiKey,'price': price,'symbol':symbol, 'type': type }
        data = self.sign(params)
        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()

    # 批量下订单
    def batch_orders(self, symbol, trade_type, order_list):
        '''
        apikey  String  是   用户申请的apiKey
        symbol  String  是   btc_usdt: 比特币
        type    String  否   买卖类型:限价单(buy/sell)
        orders_data String  是   最大下单量为5， price和amount参数参考trade接口中的说明，最终买卖类型由orders_data 中type 为准，如orders_data不设定type 则由上面type设置为准。参数格式:[{price:3,amount:5,type:'sell'},{price:3,amount:3,type:'buy'}]
        sign    String  是   请求参数的签名
        '''
        url = self.url + '/batch_trade'

        params = {'apikey': self.apiKey, 'symbol': symbol, 'type': trade_type, 'orders_data': str(order_list)}
        data = self.sign(params)

        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()

    # 批量撤销订单
    def batch_cancel_orders(self, symbol):
        '''
        apikey  String  是   公钥
        symbol  String  是   币对名称 btc_usdt:比特币
        sign    String  是   签名
        '''
        url = self.url + '/cance_all_orders'
        params = {'apikey': self.apiKey, 'symbol': symbol}
        data = self.sign(params)

        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()

    # 撤销订单
    def cancel_order(self, orderid):
        '''
        apikey  String  是   公钥
        symbol  String  是   币对名称 btc_usdt:比特币
        sign    String  是   签名
        '''
        url = self.url + '/api/publics/v1/cancel_order'
        params = {'apikey': self.apiKey, 'order_id': orderid}
        data = self.sign(params)

        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()


    # 查询订单状况
    def fetch_order(self, order_id):
        url = self.url + '/order_info'
        params = {'apikey': self.apiKey, 'order_id': order_id}
        data = self.sign(params)

        # res = requests.post(url, data=data)
        res = self.httpPost(url, data=data)
        return res.json()

        # 查询最新行情价
    def ticker(self, symbol):
         url = self.url + '/api/publics/v1/ticker'
         url+= '?symbol='+symbol
         # params = {'symbol': symbol}
         # data = self.sign(params)

         # res = requests.get(url)
         res = self.httpGet(url)
         return res.json()


# if __name__ == '__main__':
    # ex = CoinBig(apiKey, secret)
    # print(ex.userinfo())
    # print('-' * 80)
    # print(ex.account_records())