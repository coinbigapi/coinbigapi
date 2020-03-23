
# 版本号：v1.0
# 本类主要用途描述：主要进程

from CoinBigAPI import CoinBigAPI
import threading

apiKey = "apikey"
secretKey =  "secretkey"
CoinBigRestUrl ="https://www.coinbig.com"

# 币种
_symbol="btc_usdt"
_shortName1 = _symbol.split('_')[0]
_shortName2 = _symbol.split('_')[1]

# API
coinbigSpot = CoinBigAPI(CoinBigRestUrl, apiKey, secretKey)

# 币种 最新成交价
def getCBTicker():
    _cbticker = coinbigSpot.ticker(_symbol)
    if _cbticker['msg']=='success':
        _lastPrice=_cbticker['data']['ticker']['last']
        print(_lastPrice)
        return _lastPrice
    else:
        print('CB最新成交价-有错')


# 用户的账户情况
def getUsetInfo():

    _userinfo = coinbigSpot.getuserinfo()
    print(_userinfo);
    if _userinfo['msg']=='success':
        _walletCB=_userinfo['data']['info']['free'][_shortName1.upper()]
        _walletCBfreezed=_userinfo['data']['info']['freezed'][_shortName1.upper()]

        _walletUsdt=_userinfo['data']['info']['free'][_shortName2.upper()]
        _walletUsdtfreezed = _userinfo['data']['info']['freezed'][_shortName2.upper()]
        return _walletCB+_walletCBfreezed,_walletUsdt+_walletUsdtfreezed
    else:
        print('用户的账户情况-有错')




if __name__ == '__main__':

    _cbticker = threading.Thread(target=getCBTicker)
    _usetinfo = threading.Thread(target=getUsetInfo)

    _cbticker.start()
    _usetinfo.start()


