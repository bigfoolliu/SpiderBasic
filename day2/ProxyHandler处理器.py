#!-*-coding:utf-8-*-
# !@Date: 2018/11/13 17:06
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
通过自己设置的代理服务器来访问,防止本地ip被封就无法爬取
"""
import random
import urllib.request


def send_request():
    """
    发送请求
    :return:
    """
    # url = "http://httpbin.org/ip"  # 一个用于测试的网站
    url = 'https://movie.douban.com/'

    # 一个代理列表
    proxy_list = [
        # {"http": "http://maozhaojun:ntkn0npx@39.106.10.232:16818"},
        {'https': '111.195.32.103:8123'},
        {'https': '182.207.232.135:50465'},
        {'https': '122.237.107.173:80'},
        {'http': '124.235.181.175:80'},
        {'https': '222.135.92.68:38094'}
    ]

    # 随机从代理列表中挑选一个代理
    proxy = random.choice(proxy_list)
    print('[INFO]: 使用代理{}...'.format(proxy))

    # 1.构建代理 Handler 处理器对象,需要传入代理ip的列表
    proxy_handler = urllib.request.ProxyHandler(proxy)

    # 2.构建一个opener对象
    proxy_opener = urllib.request.build_opener(proxy_handler)

    # 3.使用该代理opener发送请求
    response = None
    try:
        response = proxy_opener.open(url)
    except Exception as e:
        print('[INFO]: {}'.format(e))

    return response


if __name__ == '__main__':
    for i in range(0, 100):
        resp = send_request()
        if not resp:
            print('None')
        else:
            # print(resp.read())
            print('响应成功')

