package bean

type RequestDeploy struct {        // 结构体里的字段首字母必须大写，否则无法正常解析，结构体有导出和未导出，大写字母开头为导出。
	// 在Unmarshal的时候会  根据 json 匹配查找该结构体的tag， 所以此处需要修饰符
	AccessKey string
	SecretKey string
	RequestType string
	NeedSecret bool
}

type HttpRequestType string

const (
	_ HttpRequestType = ""
	Get = "GET"
	Post = "POST"
)