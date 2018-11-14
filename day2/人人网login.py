#!-*-coding:utf-8-*-
# !@Date: 2018/11/13 19:24
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用人人网改版前的登录接口(value="http://www.renren.com/410043129/profile")
只需要用户名和密码即可登录

想做通用的模拟登录还得选别的技术，比如用内置浏览器引擎的爬虫(关键词：Selenium ，PhantomJS)
"""
import urllib.request
import urllib.parse
import http.cookiejar


def send_request():
    """
    发送请求
    :return:
    """
    post_url = "http://www.renren.com/PLogin.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/70.0.3538.77 Safari/537.36'
    }
    form_dict = {
        "email": "mr_mao_hacker@163.com",
        "password": "ALARMCHIME"
    }

    form_data = urllib.parse.urlencode(form_dict)
    request = urllib.request.Request(post_url, data=form_data.encode(), headers=headers)

    # 1. 创建一个CookJar对象来保存cookie
    cookie_jar = http.cookiejar.CookieJar()
    # 2. 使用HTTPCookieProcessor来处理cookie_jar对象
    cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
    # 3. 创建opener
    cookie_opener = urllib.request.build_opener(cookie_handler)
    # 4. 使用opener来打开url发送post请求
    response = cookie_opener.open(request)

    return response


if __name__ == '__main__':
    resp = send_request()
    print(resp.read().decode('utf-8'))
