#!-*-coding:utf-8-*-
# !@Date: 2018/11/15 12:14
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
爬取贴吧图片

1. 输入百度贴吧名
2. 按下enter键开始爬取第一页的所有帖子里的所有发布的图片
3. 按下q或者Q结束爬取

贴吧网址: https://tieba.baidu.com/
键入贴吧名搜索网址: https://tieba.baidu.com/f?ie=utf-8&kw=%E6%BC%AB%E5%A8%81&fr=search

第一页网址: https://tieba.baidu.com/f?kw=%E6%BC%AB%E5%A8%81&ie=utf-8&pn=0
第二页网址: https://tieba.baidu.com/f?kw=%E6%BC%AB%E5%A8%81&ie=utf-8&pn=50
...



每页中所有的帖子的标题跳转标签:
<a rel="noreferrer" href="/p/5950220601" title="狼叔最近是要逆天的节奏啊" target="_blank" class="j_th_tit ">
狼叔最近是要逆天的节奏啊</a>

获取到href的值然后重新发请求进入到具体的帖子



具体的一个帖子网址:
https://tieba.baidu.com/p/5950316508

具体帖子中发表的图片的标签:
<img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=61b03229a0345982c58ae59a3cf5310b/
d17eadfb43166d22b927b3c94b2309f79152d2a5.jpg" size="107599" changedsize="true" width="560" height="840">

需要获取图片的src并将图片下载保存
"""
import re
import requests


class TiebaImageSpider(object):
    """
    贴吧图片爬虫
    """
    def __init__(self):
        self.base_url = 'https://tieba.baidu.com/f?'
        self.page_base_url = 'https://tieba.baidu.com/p'
        self.page = 1
        self.query_dict = {
            'ie': 'utf-8',
            'kw': input('请输入贴吧名:'),
            'pn': str((self.page - 1) * 50)
        }
        # TODO: 使用正则则不需要考虑网站根据不同浏览器做的优化
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/70.0.3538.77 Safari/537.36'
        }
        self.pattern_page = re.compile(r'rel="noreferrer" href="/p(.*?)" title')
        self.pattern_image = re.compile(r'<img class="BDE_Image" src="(.*?)" size')

    def send_request(self, url, query_dict=None, headers=None):
        """
        发送请求,返回响应
        :param url:
        :param query_dict:
        :param headers:
        :return:
        """
        print('[INFO]: 开始发送响应...')
        response = requests.get(url, params=query_dict, headers=headers)
        return response

    def parse_page(self, response):
        """
        解析当前页面,返回所有的帖子列表
        :return:
        """
        print('[INFO]: 开始解析页面...')
        html = response.content.decode('utf-8')

        # 改为使用正则表达式
        page_link_list = self.pattern_page.findall(html)
        return page_link_list

    def parse_image(self, response):
        """
        解析帖子,获取到所有的图片地址列表
        :param response:
        :return:
        """
        print('[INFO]: 开始解析帖子中的图片链接...')

        html = response.content.decode('utf-8')
        image_url_list = self.pattern_image.findall(html)

        return image_url_list

    def save_image(self, image_response, file_name):
        """
        保存图片
        :param image_response:
        :param file_name:
        :return:
        """
        image_data = image_response.content

        print('[INFO]: 正在保存文件 {}'.format(file_name))
        with open(file_name, 'wb') as f:
            f.write(image_data)

    def run(self):
        while True:
            if input('输入(q结束):').lower() == 'q':
                break

            try:
                response = self.send_request(self.base_url, query_dict=self.query_dict, headers=self.headers)
                print('[INFO]: 响应成功...')

                page_link_list = self.parse_page(response)

                for page in page_link_list:
                    # 重新构造请求url
                    page_url = self.page_base_url + page
                    page_response = self.send_request(page_url)
                    image_url_list = self.parse_image(page_response)

                    # print(image_url_list)

                    for image_url in image_url_list:
                        image_response = self.send_request(image_url)
                        # TODO: 取图片url的最后十位数字作为图片的名称
                        file_name = 'images/' + image_url[-14:]
                        self.save_image(image_response, file_name=file_name)

            except Exception as e:
                print('[INFO]: 产生异常:{}'.format(e))

            self.page += 1


if __name__ == '__main__':
    TiebaImageSpider().run()

