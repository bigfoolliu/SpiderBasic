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

<div class="text-column-list mt10">

    <div class="text-column-item box box-790">
        <h3><a href="/article/209272.html" class="title" title="让人敬佩得目瞪口呆啊孩子">让人敬佩得目瞪口呆啊孩子</a></h3>
        <div class="desc"> 　　几个人在高尔夫更衣室，一手机响很久，一男人按了免提键。　　女：亲爱的，你在俱乐部吗?　　男：在。　　女：
        我看到一辆宝马才不到两百万。　　男人：买 。　　女：还有那个楼盘又放
        </div>
        <div class="bottom">
              <div class="time"><time class="timeago" datetime="2017-03-30.0">2年前</time><i>属于：<a href="/article/"
              class="title">内涵段子</a></i></div>
                <div class="good">92</div>
                <div class="bad">20</div>
                <div class="view">18473</div>
        </div>
    </div>

    ...

</div>
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
        # 匹配网页中所有段子内容
        # 启用DOTALL模式，让 . 也可以匹配换行符
        self.pattern_title = re.compile(r'<a href=.*? class="title" title=.*?>(.*?)</a>', re.S)
        self.pattern_content = re.compile(r'<div class="text-column-item box box-790">.*?<div class="desc">(.*?)</div>', re.S)

    def send_request(self, url, headers):
        """
        发送请求,返回响应
        :param url:
        :param headers:
        :return:
        """
        print('[INFO]: 开始发送响应 {}'.format(url))
        response = requests.get(url, headers=headers)
        return response

    def parse_content(self, response):
        """
        解析页面,获取其中的内容
        :param response:
        :return:
        """
        print('[INFO]: 开始解析当前页面...')
        html = response.content.decode('utf-8')
        title_list = self.pattern_title.findall(html)
        content_list = self.pattern_content.findall(html)
        # 将内容列表元素中的\u3000字符替换为空
        content_result_list = []
        for content in content_list:
            content_result = re.sub(r'\u3000', '', content)
            content_result_list.append(content_result)

        # 用列表推导式将标题和内容拼接为完整的段子
        result_list = [title_list[i] + '  ' + content_result_list[i] for i in range(len(title_list))]

        return result_list

    def save_file(self, result_list):
        """
        保存文本
        :param result_list:
        :return:
        """
        with open('neihan.txt', 'a') as f:
            f.write('Page{}'.format(self.page) + '\n')
            for result in result_list:
                f.write(result + '\n')
            f.write('\n\n')

    def run(self):
        """
        调度函数
        :return:
        """
        while True:
            if input('输入(q结束):').lower() == 'q':
                break

            else:
                # 根据是否为首页
                if self.page == 1:
                    full_url = self.basic_url + '.html'
                else:
                    full_url = self.basic_url + '_' + str(self.page) + '.html'

                response = self.send_request(full_url, self.headers)
                print('[INFO]: 响应成功...')

                result_list = self.parse_content(response)
                # print(result_list)

                self.save_file(result_list)

            self.page += 1


if __name__ == '__main__':
    NeihanSpider().run()
