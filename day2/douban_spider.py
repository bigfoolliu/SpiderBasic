#!-*-coding:utf-8-*-
# !@Date: 2018/11/12 20:17
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
豆瓣电影分类排行榜爬虫

1. 输入搜索的类型
剧情(11) 喜剧(24) 动作(5) 爱情(13) 科幻(17) 动画(25) 悬疑(10) 惊悚(19) 恐怖(20) 纪录片(1)
短片(23) 情色(6) 同性(26) 音乐(14) 歌舞(7) 家庭(28) 儿童(8) 传记(2) 历史(4) 战争(22)
犯罪(3) 西部(27) 奇幻(16) 冒险(15) 灾难(12) 武侠(29) 古装(30) 运动(18) 黑色电影(31)

2. 指定需要获取的页码
3. 返回所有的电影信息

https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=40&limit=20

根据查询字符串:
type: 电影类型(根据上表)
interval_id: 100:90(表示好于90%-100%的电影,序列为100:90, 95:85, 90:80, ...)
action: 无键值
start: 起始的值
limit: 单次下拉显示的电影数量
"""
import csv
import json
import urllib.request
import urllib.parse
import urllib.response


class DoubanSpider(object):
    """
    豆瓣爬虫类
    """
    def __init__(self):
        """
        初始化
        """
        self.base_url = 'https://movie.douban.com/j/chart/top_list?'
        self.headers = {
            'Accept': '*/*',
            # 本地接收压缩格式的数据，服务器传过来压缩格式gzip的文件，而解压这种gzip文件只能用deflate算法，
            # 浏览器能够自动解压，程序却不能自动解压gzip
            # 'Accept-Encoding': 'gzip, deflate, br',  # TODO: 注意该请求报头会影响接收的数据类型编码问题
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/typerank?type_name=%E9%BB%91%E8%89%B2%E7%94%B5%E5%BD%B1&type=31&\
            interval_id=100:90&action=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/70.0.3538.77 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.type = input('输入电影类型:')  # TODO: 暂时直接输入数字
        self.interval_id = '100:90'
        self.start = input('起始排名:')
        self.limit = input('抓取数量:')
        self.action = ''

    def send_request(self, url, headers):
        """
        发送请求
        :param url:
        :param headers:
        :return:
        """
        print('[INFO]: 正在向{}发送请求...'.format(url))
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        return response

    def save_file(self, file_name, content):
        """
        追加保存文件
        :param file_name: str,文件名
        :param content: bytes,保存内容
        :return:
        """
        print('[INFO]: 正在保存数据至文件{}...'.format(file_name))
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write(content)

    def dict_to_csv(self, file_name, content_dict):
        """
        将字典保存至csv文件
        :param file_name:
        :param content_dict:
        :return:
        """
        print('[INFO]: 正在保存数据至文件{}...'.format(file_name))
        with open(file_name, 'a+', encoding='utf-8') as f:
            w = csv.writer(f)
            # w.writerow(content_dict.items())  # 直接写入字典的内容
            w.writerow(content_dict.keys())  # 写入字典的键
            w.writerow(content_dict.values())  # 写入字典的值

    def run(self):
        """
        运行入口
        :return:
        """
        print('[INFO]: 程序开始运行...')
        # 构建查询字符串
        query_dict = {
            'type': self.type,
            'interval_id': self.interval_id,
            'action': self.action,
            'start': self.start,
            'limit': self.limit
        }
        query_data = urllib.parse.urlencode(query_dict)
        full_url = self.base_url + query_data

        # 发送请求返回响应
        response = None
        try:
            response = self.send_request(full_url, self.headers)
        except Exception as e:
            print('[INFO]: 返回响应异常...')
            print('[INFO]: ', e)

        # response的read()方法只能执行一次，后续执行则没有数据
        # read() 取值是 json 字符串(根据浏览器的response栏可以查看)
        json_data = response.read()
        json_str = json_data.decode('utf8')

        print('[INFO]: json_str type: ', type(json_str), len(json_str))

        # json.loads() 将json字符串转为Python数据类型
        movie_list = []
        try:
            movie_list = json.loads(json_str)  # 类型为list
        except Exception as e:
            print('[INFO]: 数据解析出现异常...')
            print('[INFO]: ', e)
        print('[INFO]: movie_list length:', len(movie_list))

        # 将结果列表数据逐条添加至文件当中
        # file_name = 'douban_result/' + self.type + self.start + self.limit + '.txt'
        file_name = 'douban_result/' + self.type + self.start + self.limit + '.csv'
        for movie_dict in movie_list:
            # self.save_file(file_name, (str(movie_dict) + '\n'))
            self.dict_to_csv(file_name, movie_dict)


if __name__ == '__main__':
    DoubanSpider().run()
