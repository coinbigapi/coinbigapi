package com.example.demo;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
import org.junit.Test;

import com.alibaba.fastjson.JSON;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Demo1 {
	private static final char HEX_DIGITS[] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
			'E', 'F' };

	@Test
	public void demo1() {
		Map<String, String> signParams = new HashMap<>();
		signParams.put("apikey", "899F4BFD47D88EC480B37095D5728C70");
		signParams.put("symbol", "btc_usdt");
		signParams.put("type", "1");
		signParams.put("size", "20");

		System.out.println(buildMysign(signParams, "84263AB49477D07D89B79C73C9D19ED9"));
	}

	/**
	 * 下单测试
	 */
	@Test
	public void demoTrade() {
		boolean isBuy = true;
		Map<String, String> signParams = new HashMap<>();
		signParams.put("apikey", "19EDB6227BED371FB475680739BD45B2");
		signParams.put("symbol", "BOPO_USDT");
		signParams.put("type", isBuy ? "buy" : "sell");

		Random random = new Random();
		int price = random.nextInt(10);
		signParams.put("price", price + "");
		signParams.put("amount", "1");
		// 请求地址：该地址为测试地址
		String url = "http://localhost:9999/api/publics/v1/trade";
		// 构建请求参数
		List<NameValuePair> params = new ArrayList<>();
		// 公钥为post请求必填参数
		params.add(new BasicNameValuePair("apikey", "19EDB6227BED371FB475680739BD45B2"));
		params.add(new BasicNameValuePair("symbol", "BOPO_USDT"));
		params.add(new BasicNameValuePair("type", isBuy ? "buy" : "sell"));
		params.add(new BasicNameValuePair("price", price + ""));
		params.add(new BasicNameValuePair("amount", "1"));
		// 构建签名，请求参数和私钥
		String sign = buildMysign(signParams, "CBD72C9A50AB8FA1EF4E902FD113E201");

		params.add(new BasicNameValuePair("sign", sign));

		String userInfo = getWeChatUserInfo(url, params);
		// 响应结果
		log.info(userInfo);

	}

	public String getWeChatUserInfo(String url, List<NameValuePair> params) {

		String result = "";
		try {
			// POST的URL
			HttpPost httppost = new HttpPost(url);
			
			httppost.setHeader("user-agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36");
			// 建立HttpPost对象
			httppost.setEntity(new UrlEncodedFormEntity(params, HTTP.UTF_8));
			
			// 通过请求对象获取响应对象
			HttpResponse response = new DefaultHttpClient().execute(httppost);

			// 判断网络连接状态码是否正常(0--200都数正常)
			if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				result = EntityUtils.toString(response.getEntity(), "utf-8");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		// System.out.println("响应结果：" + JSON.toJSONString(result));

		return result;
	}

	// 构造签名
	public String buildMysign(Map<String, String> params, String secret) {
		// 2.将待签名字符串要求按照参数名进行排序(首先比较所有参数名的第一个字母，按abcd顺序排列，若遇到相同首字母，则看第二个字母，以此类推)
		String result = createLinkString(params);

		// 将排序后的结果链接&secret_key=secretKey
		StringBuffer stringBuffer = new StringBuffer(result).append("&secret_key=").append(secret);

		// 利用32位MD5算法，对最终待签名字符串进行签名运算，从而得到签名结果字符串（MD5计算结果中字母全部大写）
		String sign = getMD5String(stringBuffer.toString());
		return sign;

	}

	/**
	 * 生成32位大写MD5值
	 */
	public static String getMD5String(String str) {
		try {
			if (str == null || str.trim().length() == 0) {
				return "";
			}
			byte[] bytes = str.getBytes();
			MessageDigest messageDigest = MessageDigest.getInstance("MD5");
			messageDigest.update(bytes);
			bytes = messageDigest.digest();
			StringBuilder sb = new StringBuilder();
			for (int i = 0; i < bytes.length; i++) {
				sb.append(HEX_DIGITS[(bytes[i] & 0xf0) >> 4] + "" + HEX_DIGITS[bytes[i] & 0xf]);
			}
			return sb.toString();
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		return "";
	}

	/**
	 * 把数组所有元素排序，并按照“参数=参数值”的模式用“&”字符拼接成字符串
	 *
	 * @param params
	 *            需要排序并参与字符拼接的参数组
	 * @return 拼接后字符串
	 */
	public static String createLinkString(Map<String, String> params) {
		List<String> keys = new ArrayList<String>(params.keySet());
		Collections.sort(keys);
		String prestr = "";
		for (int i = 0; i < keys.size(); i++) {
			String key = keys.get(i);
			String value = params.get(key);
			// 拼接时，不包括最后一个&字符
			if (i == keys.size() - 1) {
				prestr = prestr + key + "=" + value;
			} else {
				prestr = prestr + key + "=" + value + "&";
			}
		}
		return prestr;
	}
}
