#!-*-coding:utf-8-*-
# !@Date: 2018/11/13 16:52
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用自定义的opener来发送请求
"""
import urllib.request


def send_request():
    """
    发送请求返回响应
    :return:
    """
    # 构建一个HTTPHandler 处理器对象，支持处理HTTP请求,可以在此添加许多其他的参数
    http_handler = urllib.request.HTTPHandler()

    # 调用urllib.request.build_opener()方法，创建支持处理HTTP请求的opener对象
    http_opener = urllib.request.build_opener(http_handler)

    # 调用自定义opener对象的open()方法，发送request请求
    response = http_opener.open('http://www.baidu.com/')

    return response


if __name__ == '__main__':
    resp = send_request()
    print(resp)
