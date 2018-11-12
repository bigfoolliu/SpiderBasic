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
sourceText: 指着
qtv: 95916df7eace6016
qtk: SpqjpwPVRSgJ+MRkog9n5/grw1mZOEnhvYPEdrfAOaFnpz/91WsUJOwFBXBYZYDJrwHTIRPvyJgyXBt06oI1aQeX1WLVXngGcxlr/gXmiYM/qab6kyv77Z5bJbKOs5eaJiojfL+AKxNt4R1VpqjIUA==
sessionUuid: translate_uuid1541944578140
"""
import json
import urllib.parse
import urllib.request


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/70.0.3538.77 Safari/537.36'

}


def send_request(url, data):
    """
    根据请求的url和请求头等信息,发送请求并返回响应
    :param url:
    :param data: 表单提交的数据(字节类型)
    :return:
    """
    # 构造请求
    request = urllib.request.Request(url, data)
    # 发送请求获得相应
    response = urllib.request.urlopen(request)
    html_data = response.read()
    return html_data


if __name__ == '__main__':

    base_url = 'https://fanyi.qq.com/api/translate'

    original_text = input("输入中文:")

    # 构造表单字典
    form_dict = {
        'source': 'auto',
        'target': 'auto',
        'sourceText': original_text,
        'qtv': '73f42acd73f01b08',
        'qtk': '2o4hBo0KA5UKe / LusJrdmzA7yvIfYIOL1v / ZpXpFWvCm62ojREUoIKfoMSoNuesERfinGkaOVOnp5XbiBaEL3TcdjEYcm + Z6Zuh3ZF2FsyNz9WJbZShzg6FE08t9WgP4J8h5qe9TAm4zY0VuY3988w ==',
        'sessionUuid': 'translate_uuid1541946273461'
    }

    form_data = urllib.parse.urlencode(form_dict)

    print(form_data)

    html = send_request(base_url, form_data.encode())

    # 返回的是json数据需要解析
    result = json.loads(html)

    print(result['translate']['records'][0]['targetText'])
