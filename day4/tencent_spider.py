#!-*-coding:utf-8-*-
# !@Date: 2018/11/15 22:28
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用bs4
爬取腾讯招聘网的信息

https://hr.tencent.com/position.php?&start=0#a
https://hr.tencent.com/position.php?&start=10#a
https://hr.tencent.com/position.php?&start=20#a
...

多页完全爬取终结条件思路:

1. 从首页爬取到结束页
2. 判断结束页的思路:
    a. 直接根据目测网页上的数字
    b. 根据下一页按钮的状态变化为不可按压
    c. 由于爬虫不同于浏览器,可以直接继续请求下一页直至无正常响应
"""
import json

import requests
from bs4 import BeautifulSoup


class TencentSpider(object):
    """
    腾讯社招爬虫
    """
    def __init__(self):
        self.base_url = 'https://hr.tencent.com/position.php?&start='
        self.page = 1
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/70.0.3538.77 Safari/537.36'
        }
        self.job_list = []

    def send_request(self, url, headers):
        """
        发送请求,返回响应
        :param url:
        :param headers:
        :return:
        """
        print('[INFO]: 开始发送请求至 {}'.format(url))
        response = requests.get(url, headers=headers)
        return response

    def get_soup(self, response):
        """
        发送响应,获得BeautifulSoup操作对象
        :param response:
        :return:
        """
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def parse_page(self, response):
        """
        解析页面
        :param response:
        :return:
        """
        print('[INFO]: 开始解析具体页面...')

        soup = self.get_soup(response)
        job_tr_list = soup.find_all('tr', {'class': ['odd', 'even']})

        for job_tr in job_tr_list:
            job_td_list = job_tr.find_all('td')
            job_dict = {
                'job_name': job_td_list[0].a.text,
                'job_category': job_td_list[1].text,
                'job_needed_num': job_td_list[2].text,
                'job_place': job_td_list[3].text,
                'job_publish_time': job_td_list[4].text
            }
            self.job_list.append(job_dict)

        return self.job_list

    def judge_end(self, response):
        """
        判断终止条件
        :param response:
        :return:
        """
        print('[INFO]: 开始判断终止条件...')

        soup = self.get_soup(response)
        next_button = soup.find('a', {'id': 'next'})

        try:
            if next_button.attrs['class'] == ['noactive']:
                return True
        except Exception as e:
            print('[INFO]: {}'.format(e))
            return False

    def save_json(self, job_list):
        """
        保存文件为json格式
        :param job_list:
        :return:
        """
        json_str = json.dumps(job_list)
        with open('tencent.json', 'w') as f:
            f.write(json_str)

    def run(self):
        """
        调度中心
        :return:
        """
        while True:
            full_url = self.base_url + str((self.page - 1) * 10)
            response = None
            try:
                response = self.send_request(full_url, self.headers)
                print('[INFO]: 响应成功')

                self.job_list = self.parse_page(response)
                print('[INFO]: 解析页面成功')

                self.save_json(self.job_list)
                print('[INFO]: 保存json文件成功')
            except Exception as e:
                print('[INFO]: 产生异常 {}'.format(e))

            if self.judge_end(response) is True:
                break

            self.page += 1


if __name__ == '__main__':
    TencentSpider().run()
