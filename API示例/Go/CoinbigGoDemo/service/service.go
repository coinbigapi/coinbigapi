package service

import (
	"fmt"
	"encoding/json"
	. "CoinbigGoDemo/bean"
	."CoinbigGoDemo/properties"
)

func GetTicker(symbol string,request RequestDeploy)  (ticker map[string]interface{} , err error) {
	request.RequestType = Get
	request.NeedSecret = false
	params := map[string] interface{}{
		"symbol":symbol,
	}
	resultMap,err := ApiCall(TickerUrl,params,request)
	ticker = resultMap
	return
}

func GetAccount(request RequestDeploy) (account map[string]interface{},err error) {
	request.RequestType = Post
	request.NeedSecret = true
	params := map[string] interface{}{
	}
	resultMap,err := ApiCall(AccountsUrl,params,request)
	account = resultMap
	return
}
func GetDepth(symbol string,request RequestDeploy) (depth map[string]interface{},err error) {
	request.RequestType = Get
	request.NeedSecret = false
	params := map[string] interface{}{
		"symbol":symbol,
		"size":20,
	}
	resultMap,err := ApiCall(DepthUrl,params,request)
	depth = resultMap
	return
}

func TradeLimit(request RequestDeploy,exchangeType string,symbol string,amount float64,price float64)(trade map[string]interface{},err error)  {
	request.RequestType = Post
	request.NeedSecret = true
	params := map[string] interface{}{
		"type":exchangeType,
		"symbol":symbol,
		"amount":amount,
		"price":price,
	}
	resultMap,err := ApiCall(OrderLimitUrl,params,request)

	tempBytes,_ := json.Marshal(resultMap)
	fmt.Println(string(tempBytes))
	fmt.Println(err)
	trade = resultMap
	return
}

func TradeMarket(request RequestDeploy,exchangeType string,symbol string,amount float64)(trade map[string]interface{},err error)  {
	request.RequestType = Post
	request.NeedSecret = true
	params := map[string] interface{}{
		"type":exchangeType,
		"amount":amount,
		"symbol":symbol,
	}
	resultMap,err := ApiCall(OrderMarketUrl,params,request)

	tempBytes,_ := json.Marshal(resultMap)
	fmt.Println(string(tempBytes))
	fmt.Println(err)
	trade = resultMap
	return
}