# 爬虫知识

聚焦爬虫核心步骤:
1. 构造请求对象request(url, data, headers, ...)
2. 发送其请求返回response
3. 解析response(保存等)

**urllib库**

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

**Handler处理器和自定义Opener**

基本的urlopen()方法不支持代理、Cookie等其他的 HTTP/HTTPS高级功能.所以要支持这些功能:
1. 使用相关的 Handler 处理器来创建特定功能的处理器对象;
2. 然后通过 urllib.request.build_opener()方法使用这些处理器对象，创建自定义opener对象;
3. 使用自定义的opener对象，调用open()方法发送请求

**ProxyHandler处理器(代理设置)**

使用代理IP,设置一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬取.

免费代理参考:
+ [西刺免费代理IP](http://www.xicidaili.com/)
+ [快代理免费代理](http://www.kuaidaili.com/free/inha/)
+ [Proxy360代理](http://www.proxy360.cn/default.aspx)
+ [全网代理IP](http://www.goubanjia.com/free/index.shtml)

