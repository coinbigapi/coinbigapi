
#  版本号：v1.0
#  本类主要用途描述：访问CoinBig APi
from HttpUtil import buildMySign, httpGet, httpPost, GetTimeStamp


class CoinBigAPI:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey



    # 11.获取用户资产信息
    def getuserinfo(self,max_try_number=100):
        try_num = 0
        while True:
            try:
                mappingMoneyApi = "/api/publics/vip/userinfo"
                params = {}
                params['apikey'] = self.__apikey
                params['time'] = GetTimeStamp()
                params['sign'] = buildMySign(params, self.__secretkey)
                return httpPost(self.__url, mappingMoneyApi, params)
            except Exception as http_err:
                print(mappingMoneyApi, "获取用户资产信息,抓取报错", http_err)
                try_num += 1
                if try_num == max_try_number:
                     print("尝试失败次数过多，放弃尝试")
                    # return None
            else:  # 如果try里面的语句成功执行,那么就执行else里面的语句
                 if try_num >= max_try_number:
                     print("API接口，已经恢复正常运行。")

    # 18. 获取深度列表
    def getDepthList(self,symbol='',max_try_number=100):
        try_num = 0
        while True:
            try:
                depthListUrl='/api/publics/vip/depthList'

                params = ''
                if symbol:
                    params = 'symbol=%(symbol)s' % {'symbol': symbol}
                return httpGet(self.__url, depthListUrl, params)

            except Exception as http_err:
                    print(depthListUrl, "获取深度列表,抓取报错", http_err)
                    try_num += 1
                    if try_num == max_try_number:
                        print("尝试失败次数过多，放弃尝试")

                        # return None
            else:  # 如果try里面的语句成功执行,那么就执行else里面的语句
                 if try_num >= max_try_number:
                     print("API接口，已经恢复正常运行。")

    # 16. 下单交易(单个挂单)
    """itype:买卖类型: 限价单(buy / sell)
       iprice:价格
       iamount：数量
       symbol:币种 cb_usdt
    """
    def setTrade(self,itype,iprice,iamount,symbol,max_try_number=100):
        try_num = 0
        while True:
            try:
                 #print("$$$$-price="+float(iprice))
                 tradeurl="/api/publics/vip/trade"

                 params = {}
                 params['amount'] = iamount
                 params['apikey'] = self.__apikey
                 params['price'] = iprice
                 params['symbol'] = symbol
                 params['time'] = GetTimeStamp()
                 # 买卖类型: 限价单(buy / sell)
                 params['type']=itype
                 params['sign'] = buildMySign(params, self.__secretkey)
                 return httpPost(self.__url, tradeurl, params)

            except Exception as http_err:
                print(tradeurl, "下单交易(单个挂单),抓取报错", http_err)
                try_num += 1
                if try_num == max_try_number:
                    print("尝试失败次数过多，放弃尝试")
                    # return None
            else:
                 if try_num >= max_try_number:
                     print("API接口，已经恢复正常运行。")




    # 15.获取行情
    def ticker(self, symbol='',max_try_number=100):
        try_num = 0
        while True:
            try:
                TICKER_RESOURCE = "/api/publics/vip/ticker"
                params = ''
                if symbol:
                    params = 'symbol=%(symbol)s' % {'symbol': symbol}
                return httpGet(self.__url, TICKER_RESOURCE, params)

            except Exception as http_err:
                print(TICKER_RESOURCE, "获取行情,抓取报错", http_err)
                try_num += 1
                if try_num == max_try_number:
                    print("尝试失败次数过多，放弃尝试")
                    # return None
            else:  # 如果try里面的语句成功执行,那么就执行else里面的语句
                if try_num >= max_try_number:
                    print("API接口，已经恢复正常运行。")


    """
    itype:买卖类型: 限价单(buy / sell)
    orders_data:价格,数量，方向 的字典参数
    symbol:币种 cb_usdt
    """
    def GetOrderInfo(self,orderid,max_try_number=100):

        try_num = 0
        while True:
            try:
                tradeurl = "/api/publics/vip/order_detail"
                params = {}

                params['apikey'] = self.__apikey
                params['order_id'] = orderid
                params['time'] = GetTimeStamp()

                params['sign'] = buildMySign(params, self.__secretkey)
                return httpPost(self.__url, tradeurl, params)

            except Exception as http_err:
                print(tradeurl, "获取订单详情,报错", http_err)
                try_num += 1
                if try_num == max_try_number:
                    print("尝试失败次数过多，放弃尝试")
                    # return None
            else:  # 如果try里面的语句成功执行,那么就执行else里面的语句
                if try_num >= max_try_number:
                    print("API接口，已经恢复正常运行。")



