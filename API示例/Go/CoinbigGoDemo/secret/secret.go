package secret

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"coinex/utils"
	"sort"
	"strings"
	"crypto/md5"
	"io"
	"fmt"
)

func ComputeHmac256(strMessage string, strSecret string) string {
	key := []byte(strSecret)
	h := hmac.New(sha256.New, key)
	h.Write([]byte(strMessage))

	return hex.EncodeToString(h.Sum(nil))
}

func CoinbigMD5(params map[string]interface{},secretKey string) string  {
	directionMap := map[string]string{}
	keys := []string{}
	for k,v := range params{
		directionMap[k] = utils.MapToHttpGetString(map[string]interface{}{k:v})
		keys = append(keys, k)
	}
	sort.Strings(keys)
	values := []string{}
	for _,value := range keys{
		values = append(values, directionMap[value])
	}
	directionString := strings.Join(values,"&")
	directionString += ("&secret_key=" + secretKey)

	w := md5.New()
	io.WriteString(w,directionString)
	md5String := fmt.Sprintf("%x",w.Sum(nil))
	return strings.ToUpper(md5String)
}