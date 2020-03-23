#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类


import json
import hashlib
from urllib.request import urlopen, Request
from urllib import parse
import time




def buildMySign(params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    data = sign + 'secret_key=' + secretKey
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()


def httpGet(url, resource, params=''):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    request = Request(url=url + resource + '?' + params, headers=headers)
    content = urlopen(request, timeout=15).read()
    content = content.decode('utf-8')
    return json.loads(content)


def httpPost(url, resource, params):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    data = parse.urlencode(params).encode('utf-8')
    request = Request(url + resource, headers=headers, data=data)  # POST方法
    content = urlopen(request, timeout=15).read()
    content = content.decode('utf-8')

    return json.loads(content)




# 时间辍 毫秒
def GetTimeStamp():
    t = time.time()

    return int(round(t * 1000))


def md5(data):

    return  hashlib.md5(data.encode("utf8")).hexdigest().lower()





