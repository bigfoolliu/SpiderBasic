#!-*-coding:utf-8-*-
# !@Date: 2018/11/11 19:45
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
百度贴吧爬虫

1. 输入贴吧关键字
2. 输入查询的起始页码
3. 输入查询的结束页码
4. 爬取这些页码的原始数据

https://tieba.baidu.com/f?kw=%E7%88%AC%E8%99%AB&ie=utf-8&pn=100
"""
import urllib.parse
import urllib.request

import urllib3


def send_request():
    """
    发送请求
    :return:
    """
    # 输入关键字
    kw = input('输入关键字:')
    # 输入起始及结束页码
    pn_start = input('输入起始页码(从1开始):')
    pn_end = input('输入结束页码:')

    base_url = 'https://tieba.baidu.com/f?'

    # 根据起始以及结尾的页码获得各个页码
    pn_list = []
    i = 0
    while i <= (int(pn_end) - int(pn_start)):
        pn_list.append(50 * i)
        i += 1

    for pn in pn_list:
        # 构造查询字典
        query_dict = {
            'kw': kw,
            'ie': 'utf-8',
            'pn': pn
        }
        # 构建查询字符串
        query_str = urllib.parse.urlencode(query_dict)

        # 构建完整的请求url
        full_url = base_url + query_str
        print(full_url)  # TODO:

        # 构造请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        # 构造请求
        request = urllib.request.Request(full_url, headers=headers)
        # 发送请求获得相应
        response = urllib.request.urlopen(request)
        # 读取相应中的html数据
        html = response.read()

        with open('results/' + str(pn) + '.html', 'wb') as f:
            f.write(html)


if __name__ == '__main__':
    send_request()
