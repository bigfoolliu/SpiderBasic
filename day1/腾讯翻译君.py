#!-*-coding:utf-8-*-
# !@Date: 2018/11/11 21:56
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
腾讯翻译君
https://fanyi.qq.com/

翻译接口:
https://fanyi.qq.com/api/translate

请求方式:
post

提交表单数据:
source: auto
target: en
sourceText: 大
qtv: 641905a3f1cb113c
qtk: iHMVThP1aFawkmNAFLOFjAsLUGFjNFJRQns3GfrDvHhvwiq045BKL81rQQltvXrAAubdpGAwvOeK25Qbh3xvoDEQxf7o9bB3cOAopsPdIBYSRGo2qmCSLAtq0Boqg6TvITRHAsxs/h9BZ60BU7k0eg==
sessionUuid: translate_uuid1542026276453

source: auto
target: zh
sourceText: 12
qtv: cfcde856e10c710d
qtk: gzVCZo6kA+FmHCiWNR9R0qRJgF3lx2j/dSJaaAys0GgjjnhZadJtXo7N6HLuJnYAudG1eEk3VnJTJdvGxYqyHa907CmnnIaiDHHGtOVbh3RMF29ir0zudilLcczM48Apxe/Uopts4I3dCYz2wGthTQ==
sessionUuid: translate_uuid1542026220012

response:
"""
import json
import urllib.parse
import urllib.request

import time


def send_request():
    # 通过抓包找到的 post请求的url地址
    post_url = "https://fanyi.qq.com/api/translate"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",

        # 表示客户端支持的压缩格式，urllib2不支持gzip解压，但是requests和scrapy默认支持gzip解压。
        # "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",

        # 传递的表单数据的长度
        "Content-Length": "285",

        # 传递的表单数据，是通过urlencode转码后
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",

        "Cookie": "pgv_pvi=718218240; RK=kO8/hNauMo; ptcz=8a6aa2eb109c92d6aa94aa7cc0aece1190b73987b80cc71037c056b024\
        920137; pt2gguin=o0123636274; tvfe_boss_uuid=f21d3a8294e89358; mobileUV=1_15f9f25154c_a6c21; pgv_pvid=1030544\
        080; o_cookie=123636274; pac_uid=1_123636274; fy_guid=9b09602e-d2ed-4797-930d-a8054582a349; ts_uid=562838613\
        0; gr_user_id=eeb2afb3-d0b6-4e0c-ac3e-95568013e7b5; grwng_uid=3840cabe-39e3-4067-a18c-0162a15f374c; qtv=e8fb\
        dcdd4cdfc789; qtk=hZ0SKxtrrKHrmuPTyRiOGSmx0YlAWAMxomxdEG5i54X+BhnrpM+zZJtSxxWNSHzkXBMCXQWgQhj7r6uthSbnndMokR\
        1P/H/H+nPPNnO90Veu/7v46adMihj380KSpqXENEqkmSplLo3CApiarKroNQ==; pgv_info=ssid=s4222111224; ts_last=fanyi.qq.c\
        om/; openCount=1; 9c118ce09a6fa3f4_gr_session_id=dc51827c-e947-499f-af15-b4f6ac276938; 9c118ce09a6fa3f4_gr_se\
        ssion_id_dc51827c-e947-499f-af15-b4f6ac276938=true",
        "Host": "fanyi.qq.com",
        "Origin": "https://fanyi.qq.com",
        "Referer": "https://fanyi.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.353\
        8.77 Safari/537.36",
        # 表示是ajax请求
        "X-Requested-With": "XMLHttpRequest"
    }

    # 构建表单数据
    form_dict = {
        "source": "auto",
        "target": "auto",
        "sourceText": input("请输入需要翻译的文本："),
        # qtv和qtk对应Cookie里的qtv和qtv
        "qtv": "e8fbdcdd4cdfc789",
        "qtk": "hZ0SKxtrrKHrmuPTyRiOGSmx0YlAWAMxomxdEG5i54X+BhnrpM+zZJtSxxWNSHzkXBMCXQWgQhj7r6uthSbnndMokR1P/H/H+nPP\
        NnO90Veu/7v46adMihj380KSpqXENEqkmSplLo3CApiarKroNQ==",
        # 这个数据字段根据UNIX时间戳处理
        "sessionUuid": "translate_uuid" + str(int(time.time() * 1000))
    }
    form_data = urllib.parse.urlencode(form_dict)

    # 根据表单数据，更改Content-Length 长度
    headers['Content-Length'] = len(form_data)

    # 这是一个有表单数据的 post请求对象
    request = urllib.request.Request(post_url, form_data.encode(), headers)
    response = urllib.request.urlopen(request)

    # 将json字符串转为对应的Python数据类型
    json_data = json.loads(response.read())

    # 取出最后的翻译结果
    trans_text = json_data['translate']['records'][0]['targetText']
    print(trans_text)


if __name__ == '__main__':
    while True:
        send_request()

