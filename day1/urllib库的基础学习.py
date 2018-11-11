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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/70.0.3538.77 Safari/537.36'

}


def write_file(html, file_name):
    """
    将html数据写入文件
    :param html:
    :param file_name:
    :return:
    """
    with open(file_name, 'wb') as f:
        f.write(html)


def send_request(url):
    """
    根据请求的url和请求头等信息,发送请求并返回响应
    :param url:
    :return:
    """
    # 构造请求
    request = urllib.request.Request(url, headers=HEADERS)
    # 发送请求获得相应
    response = urllib.request.urlopen(request)

    return response


def tieba_spider(keyword, page_start, page_end):
    """
    贴吧爬虫
    :param keyword:
    :param page_start:
    :param page_end:
    :return:
    """
    base_url = 'https://tieba.baidu.com/f?'
    # 根据起始以及结尾的页码获得各个页码
    for page in range(int(page_start), int(page_end)):
        pn = (page - 1) * 50

        # 构造查询字典
        query_dict = {
            'kw': keyword,
            'ie': 'utf-8',
            'pn': pn
        }
        # 构建查询字符串
        query_str = urllib.parse.urlencode(query_dict)

        # 构建完整的请求url
        full_url = base_url + query_str
        print(full_url)  # TODO:
        resp = send_request(full_url)

        # 读取相应中的html数据并写入到文件
        html = resp.read()
        file_name = 'results/' + '第' + str(page) + '页.html'
        write_file(html, file_name)


if __name__ == '__main__':
    kw = input('输入要搜索的贴吧:')
    pn_start = int(input('输入起始页码(从1开始):'))
    pn_end = int(input('输入结束页码:'))

    tieba_spider(kw, pn_start, pn_end)
