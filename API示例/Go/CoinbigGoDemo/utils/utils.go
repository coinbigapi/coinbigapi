package utils

import (
	"strconv"
	"encoding/json"
	"strings"
	"math/rand"
	"time"
	"errors"
)

func MapToHttpGetString(orMap map[string]interface{}) string  {
	jsBytes,err := json.Marshal(orMap)
	if err != nil{
		panic(err)
	}
	jsString := string(jsBytes)
	jsString = strings.Replace(jsString,"{","",-1)
	jsString = strings.Replace(jsString,"}","",-1)
	jsString = strings.Replace(jsString,"\"","",-1)
	jsString = strings.Replace(jsString,",","&",-1)
	jsString = strings.Replace(jsString,":","=",-1)

	return jsString
}

func Json2map(bytes []byte) (s map[string]interface{}, err error) {

	var result map[string]interface{}
	if err := json.Unmarshal(bytes, &result); err != nil {
		return nil, err
	}
	return result,err
}

func  GetRandomString(l int) string {
	str := "0123456789abcdefghijklmnopqrstuvwxyz"
	bytes := []byte(str)
	result := []byte{}
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < l; i++ {
		result = append(result, bytes[r.Intn(len(bytes))])
	}
	return string(result)
}

type MapInterFace map[string]interface{}

func (fromMap *MapInterFace)MapInterfaceToMapString() map[string]string {
	toMap := map[string]string{}
	for k,v := range *fromMap{
		switch v.(type) {
		case string:
			toMap[k] = v.(string)
		case int64:
			toMap[k] = strconv.FormatInt(v.(int64),10)
		case float64:
			toMap[k] = strconv.FormatFloat(v.(float64),'g',-1,64)
		default:
			panic(errors.New("MapInterfaceToMapString有类型不支持"))
		}
	}
	return toMap
}

func ArrayGetSub(arr interface{},index int) interface{}  {
	return arr.([]interface{})[index]
}

func MapGetSub(ma interface{},key string) interface{}  {
	return ma.(map[string]interface{})[key]
}