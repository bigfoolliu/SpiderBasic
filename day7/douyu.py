#!-*-coding:utf-8-*-
# !@Date: 2018/11/21 21:10
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用selenium爬取斗鱼直播间的标题，主播名，观看人数

url（动态的）：
https://www.douyu.com/directory/all

标题（需要去除两边的空格）：
<h3 class="ellipsis">
                                                        衣服没买上，祖传羽绒服继续上岗了                        </h3>

主播名：
<span class="dy-name ellipsis fl">旭旭宝宝</span>

观看人数（将万替换为0000，再转换为整型）：
<span class="dy-num fr">829万</span>


点击下一页（直至完结）：
<a href="#" class="shark-pager-next">下一页</a>

<a href="#" class="shark-pager-next shark-pager-disable shark-pager-disable-next">下一页</a>
"""
# from selenium import webdriver
#
#
# driver = webdriver.Chrome()
# driver.get('https://www.douyu.com/directory/all')
#
# # 通过xpath语法来查找，会比较准确
# title_list = driver.find_element_by_xpath('//h3[@class="ellipsis"]')
#
# for title in title_list:
#     print(title)
import unittest

import time
from lxml import etree

from selenium import webdriver


class DouyuSpider(unittest.TestCase):
    """
    继承于python内置的TestCase，生成一个测试案例
    在运行时会自动的产生一些测试的相关数据
    """
    def setUp(self):
        """
        即相当于__init__(self)方法
        :return:
        """
        self.driver = webdriver.Chrome()
        self.url = 'https://www.douyu.com/directory/all'
        # self.page = int(input('输入爬取页数：'))

    def testdouyu(self):
        """
        测试的函数之前都需要添加test以供辨识
        :return:
        """
        page = 1

        # 输入url进入直播页
        self.driver.get(self.url)

        result_list = []
        while True:
            print('[INFO]: 正在解析页面 {}'.format(page))

            html = self.driver.page_source  # 获取页面源码
            html_obj = etree.HTML(html)  # 获取当前页面的操作对象

            # 获取当前页面的所有节点
            node_list = html_obj.xpath('//div[@id="live-list-content"]//div[@class="mes"]')

            for node in node_list:
                item_dict = {}
                try:
                    item_dict['title'] = node.xpath('.//h3[@class="ellipsis"]/text()')[0].strip()
                except:
                    item_dict['title'] = ''

                try:
                    item_dict['name'] = node.xpath('.//span[@class="dy-name ellipsis fl"]/text()')[0].strip()
                except:
                    item_dict['name'] = ''

                try:
                    item_dict['num'] = node.xpath('.//span[@class="dy-num fr"]/text()')[0].strip()
                except:
                    item_dict['num'] = 0

                try:
                    item_dict['num'] = item_dict['num'].replace('万', '0000')
                    if '.' in item_dict['num']:
                        item_dict['num'] = float(item_dict['num']) * 10000
                    else:
                        item_dict['num'] = float(item_dict['num'])
                except:
                    pass

                result_list.append(item_dict)

            if "shark-pager-next shark-pager-disable shark-pager-disable-next" in html:
                break

            # 点击下一页
            self.driver.find_element_by_class_name('shark-pager-next').click()

            # 为了让浏览器有时间加载页面
            time.sleep(2)

            page += 1

        # 计算观看总人数
        total_num = 0
        for item in result_list:
            total_num += item['num']
        str_time = time.strftime('%Y-%m-%d %H:%M')
        print(str_time + '斗鱼当前观看人数为: {}'.format(total_num))

        print('[INFO]: 开始保存文件至douyu.txt...')
        with open('douyu.txt', 'a+') as f:
            for item in result_list:
                try:
                    f.write(str(item))
                except:
                    f.write('当前记录有特殊字符..')
                f.write('\n')

    def tearDown(self):
        """
        类似于__del__(self)析构方法
        当爬虫结束运行(或者强制结束程序)的时候关闭浏览器对象
        :return:
        """
        self.driver.quit()


if __name__ == '__main__':
    # 注意此处测试类的写法
    unittest.main()
