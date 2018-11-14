# 爬虫知识

聚焦爬虫核心步骤:

1. 构造请求对象request(url, data, headers, ...)
2. 发送其请求返回response
3. 解析response(保存等)

**urllib库:**

```text
重要的类:
urllib.request.Request

其中三个重要的模块:
urllib.parse
urllib.request
urllib.response

对应的重要的方法:
urllib.request.urlopen()  # url打开并返回一个字节型response
urllib.parse.urlencode()  # 将一个字典转换为一个url查询字符串
urllib.parse.urlparse()  # 传入一个url对其进行解析
```

**Handler处理器和自定义Opener:**

基本的urlopen()方法不支持代理、Cookie等其他的 HTTP/HTTPS高级功能.所以要支持这些功能:

1. 使用相关的 Handler 处理器来创建特定功能的处理器对象;
2. 然后通过 urllib.request.build_opener()方法使用这些处理器对象，创建自定义opener对象;
3. 使用自定义的opener对象，调用open()方法发送请求

```python
import urllib.request

http_handler = urllib.request.HTTPHandler()
http_opener = urllib.request.build_opener(http_handler)
response = http_opener.open()
```

**ProxyHandler处理器(代理设置):**

使用代理IP,设置一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬取.
[ProxyHandler处理器.py](/day2/ProxyHandler处理器.py)

```python
import urllib.request

# 指定代理服务器
proxy = {'https': '111.195.32.103:8123'}

proxy_handler = urllib.request.ProxyHandler(proxy)
proxy_opener = urllib.request.build_opener()
response = proxy_opener.open()
```

免费代理参考:

+ [西刺免费代理IP](http://www.xicidaili.com/)
+ [快代理免费代理](http://www.kuaidaili.com/free/inha/)
+ [Proxy360代理](http://www.proxy360.cn/default.aspx)
+ [全网代理IP](http://www.goubanjia.com/free/index.shtml)

**HTTPBasicAuthHandler处理器(Web客户端授权验证):**

有些Web服务器（包括HTTP/FTP等）访问时，需要进行用户身份验证，爬虫直接访问会报HTTP 401 错误，表示访问身份未经授权.

使用特定的模块简化需要用户登录信息(cookie)的网址:

+ cookielib模块(python3中改为http.cookiejar)：主要作用是提供用于存储cookie的对象

    ```text
    该模块几个主要的对象:
    CookieJar：
          管理HTTP cookie值、存储HTTP请求生成的cookie、向传出的HTTP请求添加cookie的对象。整个cookie都存储在内存中，
          对CookieJar实例进行垃圾回收后cookie也将丢失。
    FileCookieJar (filename,delayload=None,policy=None)：
          从CookieJar派生而来，用来创建FileCookieJar实例，检索cookie信息并将cookie存储到文件中。
          filename是存储cookie的文件名。delayload为True时支持延迟访问访问文件，即只有在需要时才读取文件或在文件中存储数据。
    MozillaCookieJar (filename,delayload=None,policy=None)：
          从FileCookieJar派生而来，创建与Mozilla浏览器 cookies.txt兼容的FileCookieJar实例。
    LWPCookieJar (filename,delayload=None,policy=None)：
          从FileCookieJar派生而来，创建与libwww-perl标准的 Set-Cookie3 文件格式兼容的FileCookieJar实例。

    # python3创建一个CookieJar对象
    cookiejar = http.cookiejar.CookieJar()
  
    # python2创建一个CookieJar对象
    cookiejar = cookielib.CookieJar()

    多数情况下，我们只用CookieJar()，如果需要和本地文件交互，就用 MozillaCookjar() 或 LWPCookieJar().
    ```
+ HTTPCookieProcessor处理器：主要作用是处理这些cookie对象，并构建handler对象。

```python
import urllib.request
import http.cookiejar

# 1. 创建一个CookJar对象来保存cookie
cookie_jar = http.cookiejar.CookieJar()
# 2. 使用HTTPCookieProcessor来处理cookie_jar对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
# 3. 创建opener
cookie_opener = urllib.request.build_opener(cookie_handler)
# 4. 使用opener来打开url发送post请求
response = cookie_opener.open()
```

**Requests模块**

[参考文档](http://www.python-requests.org/en/master/)

```python
"""
requests库基本的一些用法
"""
import requests

# 添加参数
url = 'https://www.baidu.com/'
kw = {'wd':'长城'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/54.0.2840.99 Safari/537.36"}
# 根据协议类型，选择不同的代理
proxies = {"http": "http://12.34.56.79:9527"}

# 发送基本的get请求
response1 = requests.get(url=url)
# params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
response2 = requests.get("http://www.baidu.com/s?", params=kw, headers=headers)
     
# 查看响应内容,response.text 返回的是Unicode格式的数据
print(response2.text)
# 查看响应内容，response.content返回的字节流数据(常用)
print(response2.content)
# 查看完整url地址
print(response2.url)
# 查看响应头部字符编码
print(response2.encoding)
# 查看响应码
print(response2.status_code)

# 发送基本的post请求
# 返回的结果直接转换为python数据类型 
response3 = requests.post(url, data=kw, headers=headers).json()

# 使用代理(proxies参数)
response4 = requests.get(url, proxies=proxies)

# cookies
# 如果一个响应中包含了cookie，那么我们可以利用 cookies参数拿到,其返回的是一个cookiejar对象
cookie_jar = response1.cookies
# 将cookiejar对象转为字典
cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)

# session
# 这个对象代表一次用户会话：从客户端浏览器连接服务器开始，到客户端浏览器与服务器断开
ssion = requests.session()
# 发送附带用户名和密码的请求，并获取登录后的Cookie值，保存在ssion里
ssion.post("http://www.renren.com/PLogin.do", data=kw)
# ssion包含用户登录后的Cookie值，可以直接访问那些登录后才可以访问的页面
response5 = ssion.get("http://www.renren.com/410043129/profile")

# 处理HTTPS请求 SSL证书验证
# 要想检查某个主机的SSL证书，你可以使用 verify 参数（也可以不写）
response6 = requests.get(url, verify=True)
# 如果SSL证书验证不通过，或者不信任服务器的安全证书，则会报出SSLError,跳过验证即可
response7 = requests.get(url, verify=False)
```

## 结构化数据和非结构化数据提取

- 结构化数据(先有结构后有数据, 如html, json, xml)
- 非结构化数据(先有数据后有结构, 如txt, js, css, 图片, 音视频)

**正则表达式re模块**

[正则表达式参考手册](http://tool.oschina.net/uploads/apidocs/jquery/regexp.html)
[正则表达式教程](http://www.runoob.com/regexp/regexp-syntax.html)

```python
import re

pattern = re.compile(r'^$')  # 创建一个模式pattern对象
result = pattern.findall('hello\nworld')  # 利用pattern对象来查找,返回一个列表

"""
pattern对象的其他方法:
match 方法：从起始位置开始查找，一次匹配, 可以指定位置, m.group()返回具体的数据
search 方法：从任何位置开始查找，一次匹配
findall 方法：全部匹配，返回列表
finditer 方法：全部匹配，返回迭代器
split 方法：分割字符串，返回列表
sub 方法：替换
"""
```

**XPath**

XPath(XML Path Language)是一门在XML文档中查找信息的语言,可用来在XML文档中对元素和属性进行遍历。

[XPath教程](http://www.w3school.com.cn/xpath/index.asp)

