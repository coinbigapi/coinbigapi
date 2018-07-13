package service

import (
	"fmt"
	"net/http"
	"io/ioutil"
	"errors"
	. "CoinbigGoDemo/bean"
	. "CoinbigGoDemo/utils"
	"net/url"
	."CoinbigGoDemo/properties"
	"strings"
	"time"
	."CoinbigGoDemo/secret"
)

func proxyRequest(req *http.Request)(resp *http.Response, err error) {
	proxy := func(_ *http.Request) (*url.URL, error) {
		return url.Parse("http://127.0.0.1:8888")//根据定义Proxy func(*Request) (*url.URL, error)这里要返回url.URL
	}
	transport := &http.Transport{Proxy: proxy}
	client := &http.Client{Transport: transport}
	return client.Do(req)
}

func getRequest(request RequestDeploy,requestUrl string,params map[string]interface{}) (resp *http.Response, err error) {

	if params != nil {
		requestUrl = fmt.Sprintf("%s?%s",requestUrl,MapToHttpGetString(params))
	}

	req, err := http.NewRequest(request.RequestType, requestUrl, nil)
	if err != nil {
		return nil, err
	}
	//return proxyRequest(req)
	return 	http.DefaultClient.Do(req)
}

func postRequest(request RequestDeploy,requestUrl string,params MapInterFace) (resp *http.Response, err error) {

	//paramsHttpString,_:= json.Marshal(params)
	var clusterinfo = url.Values{}
	stringMap := params.MapInterfaceToMapString()
	for k,v := range stringMap{
		clusterinfo.Add(k,v)
	}
	data := clusterinfo.Encode()
	req, err := http.NewRequest(request.RequestType, requestUrl, strings.NewReader(string(data)))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	//return proxyRequest(req)
	return 	http.DefaultClient.Do(req)
}

func ApiCall(url string,params map[string]interface{},request RequestDeploy) (map[string]interface{}, error) {

	var requestUrl string

	if params == nil && request.NeedSecret {
		params = map[string]interface{}{}
	}

	if request.NeedSecret {
		params["apikey"] = request.AccessKey
		params["time"] = time.Now().UnixNano()/1000000
		params["sign"] = CoinbigMD5(params,request.SecretKey)
	}

	requestUrl = fmt.Sprintf("%s%s",BaseURL,url)

	fmt.Println(requestUrl)
	var resp *http.Response
	var err error
	switch request.RequestType {
	case Get:
		resp, err = getRequest(request,requestUrl,params)
	case Post:
		resp, err = postRequest(request,requestUrl,params)
	default:
		panic(errors.New("核心网络访问暂时只支持Get和Post"))
	}

	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	returnMap,err := Json2map(b)
	if returnMap["status"] != nil{
		panic(errors.New(string(b)))

	}

	if returnCode := returnMap["code"];returnCode.(float64) != 0{
		panic(errors.New(string(b)))
	}
	return returnMap,err
}