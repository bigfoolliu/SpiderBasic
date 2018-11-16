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
import requests
from bs4 import BeautifulSoup


class TencentSpider(object):
    """
    腾讯社招爬虫
    """
    def __init__(self):
        self.base_url = 'https://hr.tencent.com/position.php?&start='
        self.page = 280
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/70.0.3538.77 Safari/537.36'
        }

    def send_request(self, url, headers):
        print('[INFO]: 开始发送请求至 {}'.format(url))
        response = requests.get(url, headers=headers)
        return response

    def parse_title(self, response):
        print('[INFO]: 开始解析头部...')
        html = response.content.decode('utf-8')

        soup = BeautifulSoup(html, 'lxml')
        header_list = soup.find('tr', {'class': 'h'}).find_all('td')

        print(header_list, type(header_list))

        header_dict = {
            'job_name': header_list[0].text,
            'job_category': header_list[1].text,
            'job_needed_num': header_list[2].text,
            'job_place': header_list[3].text,
            'job_publish_time': header_list[4].text
        }

        return header_dict

    def parse_page(self, response):
        print('[INFO]: 开始解析具体页面...')

        html = response.content.decode('utf-8')

        soup = BeautifulSoup(html, 'lxml')
        job_tr_list = soup.find_all('tr', {'class': ['odd', 'even']})

        job_list = []
        for job_tr in job_tr_list:
            job_td_list = job_tr.find_all('td')
            job_dict = {
                'job_name': job_td_list[0].a.text,
                'job_category': job_td_list[1].text,
                'job_needed_num': job_td_list[2].text,
                'job_place': job_td_list[3].text,
                'job_publish_time': job_td_list[4].text
            }
            job_list.append(job_dict)

        return job_list

    def judge_end(self, response):
        print('[INFO]: 开始判断终止条件...')

        html = response.content.decode('utf-8')

        soup = BeautifulSoup(html, 'lxml')

        next_button = soup.find('a', {'id': 'next'})

        try:
            if next_button.attrs['class'] == ['noactive']:
                return True
        except Exception as e:
            print('[INFO]: {}'.format(e))
            return False

    def save_json(self):
        pass

    def run(self):
        while True:
            full_url = self.base_url + str((self.page - 1) * 10)
            response = None
            try:
                response = self.send_request(full_url, self.headers)
                print('[INFO]: 响应成功')

                if self.page == 1:
                    header_dict = self.parse_title(response)
                    print('[INFO]: 解析头部成功')

                job_list = self.parse_page(response)
                print('[INFO]: 解析页面成功')
            except Exception as e:
                print('[INFO]: 产生异常 {}'.format(e))

            if self.judge_end(response) is True:
                break

            self.page += 1


if __name__ == '__main__':
    TencentSpider().run()
