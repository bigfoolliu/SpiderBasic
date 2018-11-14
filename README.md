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
    ```
