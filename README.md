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

```python
"""
lxml模块通过xpath来进行数据解析的基本步骤

xpath核心语法:
/       从根节点选取
//      从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置
@       选取属性
[]      当前节点下的某些属性
..      选取当前节点的父节点
"""
from lxml import etree


def parse(response):
    html = response.content
    
    # 构造一个HTML的可操作对象
    html_obj = etree.HTML(html)
    # 通过xpath函数查找,返回的是一个列表
    page_link_list = html_obj.xpath("//a[@class='j_th_tit ']/@href")  # 提取属性
    page_text_list = html_obj.xpath("//a[@class='j_th_tit ']/text()")  # 提取文本
    
    return page_link_list, page_text_list
```

**CSS 选择器：BeautifulSoup4**

lxml只会局部遍历, Beautiful Soup是基于HTML DOM的，会载入整个文档, 性能相对较低.
BeautifulSoup 用来解析 HTML比较简单，API非常人性化，支持CSS选择器、Python标准库中的HTML解析器，也支持 lxml的 XML解析器.

[bs4官方文档](http://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

```python
"""
bs4使用基本流程:

Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:
Tag                 也就是HTML中的一个个标签,两个重要的属性，是 name(名字) 和 attrs(属性)
NavigableString     代表获取标签内部的文字对象
BeautifulSoup
Comment
"""
from bs4 import BeautifulSoup

html = '<div class="title"><a src="https://www.baidu.com/"></a></div>'

# 构造一个BS对象,并指定解析器为lxml
soup = BeautifulSoup(html, 'lxml') 

print(soup.prettify())  # 以bs的格式格式化输出soup对象的内容

# 获得所有class为title或者content的div标签, 返回结果为列表
node_list = soup.find_all('div', {'class': ['title', 'content']})
# 获得a标签的列表
node_list2 = soup.select('a')
# 获得首个a标签的所有属性
attrs_list = soup.select('a')[0].attrs
# 获得首个a标签的文本
text1 = soup.select('a')[0].text  # 如果内容为注释则不会获取
text2 = soup.select('a')[0].string  # 即使是注释也会获得文本
```

**数据提取之JSON与JsonPATH**

python内置模块json的相关操作

```python
"""
使用python自带的json模块将python对象与json字符串进行转换存储

对照表
json        python
object      dict
array       list
string      unicode
number(int) int, long
number(real) float
true        True
false       False
null        None
"""
import json

# 实现python类型转化为json字符串，返回一个str对象 把一个Python对象编码转换成Json字符串
# 处理中文时，添加参数 ensure_ascii=False 来禁用ascii编码 
str_list1 = [1, 2, 3] 
json.dumps(str_list1)  # 结果为json字符串: '[1, 2, 3]'

# loads()把Json格式字符串解码转换成Python对象
str_list2 = '[1, 2, 3]'
json.loads(str_list2)  # 结果为python列表: [1, 2, 3]

# dump()将Python内置类型序列化为json对象后写入文件
dictStr = {"city": "北京", "name": "大刘"}
json.dump(dictStr, open("dictStr.json","w"), ensure_ascii=False)

# 读取文件中json形式的字符串元素 转化成python类型
strDict = json.load(open("dictStr.json"))
```

**JsonPath**

JsonPath 是一种信息抽取类库，是从JSON文档中抽取指定信息的工具.
[JsonPath官方文档](Jhttp://goessner.net/articles/JsonPath/)

```text
JsonPath与XPath语法对比：
Json结构清晰，可读性高，复杂度低，非常容易匹配，下表中对应了XPath的用法。

XPath	JSONPath	描述
/	    $	        根节点
.	    @	        现行节点
/	    .or[]	    取子节点
..	    n/a	        取父节点，Jsonpath未支持
//	    ..	        就是不管位置，选择所有符合条件的条件
*	    *	        匹配所有元素节点
@	    n/a	        根据属性访问，Json不支持，因为Json是个Key-value递归结构，不需要属性访问。
[]	    []	        迭代器标示（可以在里边做简单的迭代操作，如数组下标，根据内容选值等）
|	    [,]	        支持迭代器中做多选。
[]	    ?()	        支持过滤操作.
n/a	    ()	        支持表达式计算
()	    n/a	        分组，JsonPath不支持
```

```python
"""
通过jsonpath模块中的jsonpath函数来进行数据抽取
"""
from jsonpath import jsonpath

python_obj = [{}, {}]  # json字符串转换后的python对象
result_list = jsonpath(python_obj, '$..name')  # 找到根节点下的所有匹配的key值为name的
```

**MongoDB**

可扩展的高性能，开源，模式自由，面向文档的NoSQL，基于分布式文件存储，由 C++ 语言编写.
使用的是内存映射存储引擎，它会把磁盘IO操作转换成内存操作.
既拥有Key-Value存储方式的高性能和高度伸缩性，也拥有传统的RDBMS系统的丰富的功能.

[MongoDB官方文档](https://docs.mongodb.com/)
[MongoDB中文社区](http://www.mongoing.com/)

常见数据类型:

```text
ObjectID    文档id
String      字符串(utf-8)
Boolean     布尔值,true或false
Integer     整数可以是32位或64位，这取决于服务器
Double      浮点值
Arrays      数组或列表，多个值存储到一个键    
Object      用于嵌入式的文档，即一个值为一个文档
Null        存储Null值
Timestamp   时间戳，表示从1970-1-1到现在的总秒数
Date        日期, 存储当前日期或时间的UNIX时间格式, 创建日期语句: Date('2017-12-20'))
```

常用命令:

```text
数据库命令:
    db  # 查看当前使用的数据库
    show dbs  # 查看所有的数据库
    user db1  # 切换数据库为db1
    db.dropDatabase()  # 删除当前使用的数据库

集合命令:
    db.createCollection("stu")  # 创建一个集合stu(类似表的概念)
    show collections  # 展示所有的集合
    db.stu.drop()  # 删除集合stu

插入数据命令:
    db.stu.insert({name: 'liu', age: 20})

更新数据命令:
    db.stu.update({age: 20}, {age: 21})  # 全文档更新
    db.stu.update({age: 20}, {$set: {age: 21}})  # 指定属性更新，通过操作符$set
    db.stu.update({age: 20}, {$set: {gender: 'man'}}, {multi: true})  # 修改多条匹配到的数据

保存数据命令:
    db.stu.save({_id: 2, name: liu})  # _id存在则修改,不存在则创建

查询数据命令:
    db.stu.find({name: 'liu'})  # 查询所有符合条件的
    db.stu.findOne({name: 'liu'})  # 查询符合条件的第一个
    db.stu.find({age: {$gt: 10}}).skip(1)  # 跳过结果中的第一个,显示其他结果
    db.stu.find({age: {$gt: 10}}).limit(2)  # 显示结果的前两个
    db.stu.find({age: {$gt: 10}}).skip(1).limit(2)  # 找到结果中跳过第一个显示接下来的2个,且skip与limit顺序不影响结果

投影显示:
    指定显示字段和不显示字段, 指定find第二个参数,通过1和true指定显示, 0和false指定不显示, 默认_id一定显示
    db.stu.find({}, {name: 1, hometown: false})  # 结果中显示name, 不显示hometown

sort()排序:
    通常按照数字排序, 字符串的话按照首字母的ASCII码值排序
    db.stu.find().sort({age: 1})  # 结果中按照年龄升序显示

count()统计个数:
    db.stu.find({age: {$lt: 20}}).count()  # 计算年龄小于20的结果的个数
    db.stu.count({age: {$lt: 20}})  # 第二种用法

distinct()去重显示:
    db.stu.distinct('hometown')  # 显示一个hometown的列表
    db.stu.distinct('hometown', {age: {$lt: 20}})  # 添加条件的去重


比较运算符:
    默认     等于
    $gt     大于
    $gtq    大于等于
    $lt     小于
    $ltq    小于等于
    $ne     不等于

逻辑运算符:
    $and    与
    $or     或

范围运算符:
    $in     在
    $nin    不在

支持正则表达式:
    $regex      正则表达式
    $options    其他参数
    $i          大小写忽略
    $s          换行符忽略
    db.stu.find({name: {$regex: '^Big'}, $options: '$i'})

自定义函数查询:
    db.stu.find({$where : function() { return this.age != 20 }


聚合运算:
    db.集合名称.aggregate([ {管道 : {表达式}} ])
    第一个管道的输出将作为第二个管道的输入
    
    常用管道：
        $group：将集合中的文档分组，可用于统计结果
        $match：过滤数据，只输出符合条件的文档
        $project：修改输入文档的结构，如重命名、增加、删除字段、创建计算结果
        $sort：将输入文档排序后输出
        $limit：限制聚合管道返回的文档数
        $skip：跳过指定数量的文档，并返回余下的文档
        $unwind：将数组类型的字段进行拆分
    
    aggregate([{$match}, {$group}, {}])
    
    $group分组统计方法
        $sum：计算总和，$sum:1同count表示计数
        $avg：计算平均值
        $min：获取最小值
        $max：获取最大值
        $push：在结果文档中插入值到一个数组中
        $first：根据资源文档的排序获取第一个文档数据
        $last：根据资源文档的排序获取最后一个文档数据
    
    # 按年龄分组，输出各组的年龄的总和
    db.stu.aggregate([
        {
            $group: {
                _id: “$gender”,  # 指定分组的依据
                sum_age: {$sum: “$age”}  # 指定的输出字段，结果为是对上方分组的age的求和
            }
        }
    ])
    
    # 查询年龄大于20的男生、女生人数
    db.stu.aggregate([
        {$match:{age:{$gt:20}}},
        {$group:{_id:'$gender',counter:{$sum:1}}}  # $sum后接1表示统计个数
    ])
    
    # 查询学生的姓名、年龄
    db.stu.aggregate([
        {$project:{_id:0,name:1,age:1}}
    ])


索引：
    使用explain()命令进行查询性能分析(在数据量比较大的情况下)
    db.t1.find({name:'test10000'}).explain('executionStats')
    
    db.t1.ensureIndex({name:1},{"unique":true})  # 创建索引，1表示升序，-1表示降序,建立唯一索引，实现唯一约束的功能
    db.t1.getIndexes()  # 查看文档所有索引
    db.t1.dropIndexes('索引名称')  # 删除索引


数据库备份与恢复：
    备份：
        mongodump -h dbhost -d dbname -o dbdirectory
        -h：服务器地址，也可以指定端口号
        -d：需要备份的数据库名称
        -o：备份的数据存放位置，此目录中存放着备份出来的数据
    恢复：
        mongorestore -h dbhost -d dbname --dir dbdirectory
        -h：服务器地址
        -d：需要恢复的数据库实例
        --dir：备份数据所在位置
```

在python代码中如何实现：

```python
"""
在python中连接和操作MongoDB数据库
基本上的语法和直接操作相同，注意：
    1. 相同的方法，如sort的处理
    2. 返回的对象可迭代的处理
    3. 参数需要加引号
"""
import pymango

client = pymango.MongoClient()  # 创建一个客户端对象，默认连接本地的数据库(可以指定ip和端口)
db = client.test  # 创建一个数据库对象
stu = db.stu  # 创建一个collections集合对象


"""
主要方法如下
    insert_one：加入一条文档对象
    insert_many：加入多条文档对象
    find_one：查找一条文档对象
    find：查找多条文档对象
    update_one：更新一条文档对象
    update_many：更新多条文档对象
    delete_one：删除一条文档对象
    delete_many：删除多条文档对象
"""

result_list = list(stu.find())  # find()的结果为可迭代对象

# 使用投影，方法一致
result_list1 = list(stu.find({'age': {'$gt': 18}}, {'name': 1, 'age': 1}))

# sort方法由于和python的方法重复，所以以参数的形式使用，按年龄升序排列
result_list2 = list(stu.find({'age': {'$gt': 18}}, {'name': 1, 'age': 1}, sort=[('age', 1)]))
```

Tips：

```python
"""
python列表的排序
"""
list1 = [1, 12, 5, 13, 4]

list1.sort(reverse=True)  # 此种排序会直接影响更改原始的列表
sorted(list1)  # 此种排序不会更改原始列表，会产生新的列表

# 对多重列表或者列表嵌入字典的排序
list2 = [[1, 23], [12, 4]]
list3 = [{'name': 'a', 'age': 10}, {'name': 'b', 'age': 6}, {'name': 'c', 'age': 12}]

sorted(list2)  # 默认是对内部列表的第一个元素进行排序
sorted(list2, key=lambda item: item[1])  # 添加参数，并使用lambda函数更改按下标1排序 
sorted(list3, key=lambda item: item['age'])  # 对传入的每一个列表中的元素，取下标'age'
```
