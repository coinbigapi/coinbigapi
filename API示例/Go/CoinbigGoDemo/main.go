package main

import (
	"CoinbigGoDemo/bean"
	"CoinbigGoDemo/service"
	"fmt"
)

func main() {
	var request = bean.RequestDeploy{
		"",
		"",
		bean.Get,
		false,
	}

	defer func() {
		if e := recover(); e != nil {
			if ee,ok := e.(error);ok {
				e = ee.Error()
			}
			fmt.Println(e)
		}
	}()

	fmt.Println("测试获取账户资产")
	fmt.Println(service.GetAccount(request))
	fmt.Println("测试获取市场行情")
	fmt.Println(service.GetTicker("btc_usdt",request))
	fmt.Println("测试获取市场深度")
	fmt.Println(service.GetDepth("btc_usdt",request))
	//fmt.Println("测试限价单")
	//fmt.Println(service.TradeLimit(request,"buy","btc_usdt",0.01,0.01))
	fmt.Println("测试市价单")
	fmt.Println(service.TradeMarket(request,"buy_market","btc_usdt",0.01))
}