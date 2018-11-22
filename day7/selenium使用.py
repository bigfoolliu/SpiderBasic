#!-*-coding:utf-8-*-
# !@Date: 2018/11/21 20:11
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
selenium自动化测试工具的使用

注意：
selenium打开一个浏览器对象之后，在浏览器中的操作和使用python代码操作的结果是一样的
"""
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys

url_list = [
    'http://www.baidu.com/',
]


driver = webdriver.Chrome()
driver.get(url_list[0])  # 打开的是一个完全加载的页面
# html = driver.page_source  # 获取网页的源码

# driver.quit()  # 关闭浏览器对象

# 找到关键字输入框和搜索按钮
# html_obj = etree.HTML(html)
# kw = html_obj.xpath('//input[@id="kw"]')[0]
# su = html_obj.xpath('//input[@id="su"]')[0]


# 向输入框中输入关键字,并按下回车键
# kw = driver.find_element_by_id('kw')
# kw.send_keys('python')
# time.sleep(2)
# kw.send_keys(Keys.ENTER)

# 找到新闻链接并点击
news = driver.find_element_by_name('tj_trnews')
news.click()

title = driver.title

print(title)

time.sleep(5)

driver.quit()
