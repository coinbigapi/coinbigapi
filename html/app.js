var ws=null;
/* 创建一个方法,用来连接我们的websocket服务 */
function connection(url) {
	if ("WebSocket" in window) {
		console.log("您的浏览器支持 WebSocket!");
		// 打开一个 web socket
		 ws = new WebSocket(url);
 		ws.onopen = function(){
                  // Web Socket 已连接上，使用 send() 方法发送数据
            console.log("数据发送中...");
         };
		
		ws.onmessage = function(evt) {
			var fr = new FileReader();
         	fr.readAsBinaryString(evt.data, "UTF-8");
         	fr.onload = function () {
		        var unit8 = fr.result;
		        //获取压缩后的字符串
		        var inflator = new pako.Inflate();
		        inflator.push(unit8, true);
		        //解压完成，生成
		        var re = inflator.result;
		        var strData = String.fromCharCode.apply(null, new Uint16Array(re));
		        var result = $.parseJSON(strData);
		        //console.info(result);
                  console.info(result.data);
                  console.info(result.datatype);
            }
		};
	
	}else {
		// 浏览器不支持 WebSocket
		alert("您的浏览器不支持 WebSocket!");
	}
};

function sendMsg(type){
	 ws.send('{"datatype":"'+type+'","data":27}}');
	 
	
}
