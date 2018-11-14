#!-*-coding:utf-8-*-
# !@Date: 2018/11/14 20:27
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用正则表达式爬取该网站的文章:

https://www.neihan8.com/article/index.html
https://www.neihan8.com/article/index_2.html
https://www.neihan8.com/article/index_3.html

需求:
从第一页开始爬取,按下enter爬取一页,按q结束爬取

需要用正则表达式从以下的标签中提取出其中的内容:

<div class="text-column-item box box-790">
        <h3><a href="/article/209253.html" class="title" title="叫警察">叫警察</a></h3>
        <div class="desc"> 　　年轻人在饭店吃霸王餐，吃完了不付钱就想离开，被服务员逮住。　　服务员威胁说：“5分钟内，你再不付钱，
        我就叫警察了。”　　年轻人无所谓地说：“你以为警察来了会替我付钱吗?</div>
        <div class="bottom">
              <div class="time"><time class="timeago" datetime="2017-03-30.0"></time><i>属于：<a href="/article/"
              class="title">内涵段子</a></i></div>
                <div class="good" >17</div>
                <div class="bad" >11</div>
                <div class="view" >9250</div>
            </div>
      </div>

解析内容时需要将部分的数据删除:
 　　乘地铁遇到个牛人。　　地铁上，一哥们儿的铃声大作，众乘客一听： “爷爷，那孙子又给您来电话了&amp;hellip; 爷爷，
 那孙子又给您来电话了&amp;hellip; 爷爷，那孙子又给您来电话了。”
"""
import re

import requests


class NeihanSpider(object):
    """
    内涵吧内涵段子爬虫
    """
    def __init__(self):
        self.basic_url = 'https://www.neihan8.com/article/index'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/70.0.3538.77 Safari/537.36'
        }
        self.page = 1
        self.pattern = re.compile(r'<div class="desc">(.+?)</div>')  # 构建一个匹配段子内容的正则表达式

        # 匹配网页中无用字符：
        # \s 表示空白字符（如\n \r 空格等）
        # <.*?> 表示标签 （如 <p> <br>等）
        # &.*?; 表示HTML实体字符（如 &nbsp;等）
        # 　 或 u"\u3000".encode("utf-8") 表示中文全角空格，无法被\s匹配
        # self.pattern_content = re.compile(r"\s|<.*?>|&.*?;|　")
        self.pattern_content = re.compile(r"\s|<.*?>|&.*?;|" + u"\u3000")

    def send_request(self, url):
        """
        发送请求,返回响应
        :param url:
        :return: response 字节流
        """
        response = requests.get(url, headers=self.headers)
        return response

    def parse_content(self, response):
        """
        解析response中的内容
        :param response: 字节流
        :return: list
        """
        html = response.content.decode('utf-8')
        content_list = self.pattern.findall(html)
        return content_list

    def save_file(self, content_list, file_name):
        """
        将内容列表存储至文件
        :param content_list:
        :param file_name:
        :return:
        """
        print('[INFO]: 开始向{}写入数据...'.format(file_name))
        with open(file_name, 'a') as f:
            for content in content_list:
                # 将单条记录content中的无用内容删除掉,即数据清洗
                content_result = self.pattern_content.sub('', content)
                f.write(content_result)
                f.write('\n')

    def run(self):
        """
        调度函数
        :return:
        """
        while True:
            # 输入的为q或者Q时结束爬取
            if input('输入(q结束):').lower() == 'q':
                break

            # 输入换行时开始爬取一页的内容
            if self.page == 1:
                full_url = self.basic_url + '.html'
            else:
                full_url = self.basic_url + '_' + str(self.page) + '.html'

            response = None
            try:
                response = self.send_request(full_url)
                print('[INFO]: 发送请求至{}成功...'.format(full_url))
            except Exception as e:
                print('[INFO]: 请求发生异常{}'.format(e))

            content_list = self.parse_content(response)

            file_name = 'neihan8/Page' + str(self.page) + '.txt'
            self.save_file(content_list, file_name)

            self.page += 1


if __name__ == '__main__':
    NeihanSpider().run()
