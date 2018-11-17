#!-*-coding:utf-8-*-
# !@Date: 2018/11/16 15:30
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
爬取拉勾网的职位信息

首页: https://www.lagou.com/
提交地址: self.post_url = "https://www.lagou.com/jobs/positionAjax.json?"

总的查询条件:
    xl: 本科                          学历# ['全职', '实习']
    jd: 未融资                         阶段# ['未融资', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资']
    hy: 移动互联网                     行业# ['移动互联网', '电子商务', '金融', '企业服务', '教育', '文化娱乐', '游戏', 'O2O',
                                            '硬件', '社交网络','旅游', '医疗健康', '生活服务', '信息完全', '数据服务',
                                            '广告营销', '分类信息', '招聘', '其他', '区块链', '人工智能']
    px: default                       排序(new表示按最新)# 排序按默认方式, ['default', 'new']
    gx: 全职                          工(作)性(质)# ['全职', '实习']
    gm: 50-150人                      规模# ['少于15人', '15-50人', '50-150人', '150-500人', '500-2000人', '2000人以上']
    city: 深圳                        城市# 城市默认为全国
    district: 南山区                   区
    needAddtionalResult: false        其他条件
    isSchoolJob: 1                    是否为校招工作

2. 获取到json文件的信息,并保存到csv的文件中

返回的其中一条json字段(抓包得到):
    {
          "companyId": 173177,
          "positionName": "python开发",
          "workYear": "3-5年",
          "education": "本科",
          "jobNature": "全职",
          "longitude": "113.331592",
          "latitude": "23.115529",
          "financeStage": "天使轮",
          "companySize": "50-150人",
          "companyLogo": "i/image/M00/1B/42/CgpFT1kJVXyALGLxAAFexBnuhDs088.png",
          "industryField": "游戏",
          "companyShortName": "BBGAME",
          "city": "广州",
          "salary": "10k-15k",
          "positionId": 5297689,
          "positionAdvantage": "晋升快,薪资高,福利好,上司nice",
          "createTime": "2018-11-15 16:01:28",
          "district": "天河区",
          "score": 0,
          "approve": 1,
          "positionLables": [],
          "industryLables": [],
          "publisherId": 9168390,
          "companyLabelList": [
            "年底双薪",
            "绩效奖金",
            "领导好",
            "扁平管理"
          ],
          "businessZones": null,
          "formatCreateTime": "2天前发布",
          "companyFullName": "广州黑胡子游戏开发有限公司",
          "adWord": 0,
          "gradeDescription": null,
          "promotionScoreExplain": null,
          "firstType": "开发|测试|运维类",
          "secondType": "后端开发",
          "isSchoolJob": 0,
          "subwayline": "APM线",
          "stationname": "妇儿中心",
          "linestaion": "3号线_广州塔;3号线_珠江新城;5号线_珠江新城;5号线_猎德;5号线_潭村;APM线_海心沙;APM线_大剧院;APM线_花城大道;APM线_妇儿中心;APM线_黄埔大道",
          "thirdType": "Python",
          "skillLables": [],
          "hitags": null,
          "resumeProcessRate": 6,
          "resumeProcessDay": 1,
          "imState": "today",
          "lastLogin": 1542417618000,
          "explain": null,
          "plus": null,
          "pcShow": 0,
          "appShow": 0,
          "deliver": 0
    },

"""
import csv
import json

import requests
from jsonpath import jsonpath


class LagouSpider(object):
    """
    拉钩爬虫页面测试:
    1. 页面分析就是检查网址的的变化
    2. 换页网址变化就是静态页面, 则直接通过html获取数据
    3. 换页网址不发生变化则是动态页面, 需要通过抓包
    """
    def __init__(self):
        self.post_url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.page = 1
        # 提交表单字典
        self.form_dict = {
            'first': 'true',  # 是否为第一次访问
            'pn': self.page,  # 页码
            'kd': input('输入查询关键字:'),  # 查询关键字
        }
        # 查询字典
        self.query_dict = {
            'xl': '',
            'jd': '',
            'hy': '',
            'px': 'default',
            'gx': '',
            'gm': '',
            'city': '全国',
            'district': '',
            'needAddtionalResult': 'false',
            'isSchoolJob': '1'  # 默认为校招工作
        }
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "25",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "user_trace_token=20170923184359-1ba5fe6f-a04c-11e7-a60e-525400f775ce; LGUID=20170923184359-1ba60\
            10d-a04c-11e7-a60e-525400f775ce; _ga=GA1.2.136733168.1506163440; _gid=GA1.2.1817431977.1542253084; index_lo\
            cation_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAAAGGABCB7F613FC0F51CAA33DF26E0E75306A26D; LGSID=20181115172902-e3666046-e8b8-11e8-9f7e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542253085,1542274142; TG-TRACK-CODE=index_search; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542274641; LGRID=20181115173720-0caa6b7e-e8ba-11e8-9f7f-525400f775ce; SEARCH_ID=b19bd022583241c883c3f0bc93cf6d3e",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            # TODO: 当网站响应ip异常不一定就是封了ip,需要检查请求头的问题
            # 1. 反爬点1(防盗链, list_后需要接职位列表才可以)
            # "Referer": "https://www.lagou.com/jobs/list_" + self.form_dict['kd'],
            "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
            # 2. 反爬点2
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest"
        }

    def send_request(self, url, headers, query_dict=None, form_dict=None):
        """
        发送请求,返回响应
        :param url:
        :param headers:
        :param query_dict: 查询字典
        :param form_dict: 查询字典
        :return:
        """
        print('[INFO]: 开始发送请求至{}, 页码:{}'.format(url, self.page))
        # post请求要传入url, 查询参数params, 表单数据data, 请求头headers
        response = requests.post(url, params=query_dict, data=form_dict, headers=headers)
        return response

    def parse_page(self, response):
        """
        使用jsonpath解析页面,
        返回其中的职位信息
        :param response:
        :return:
        """
        print('[INFO]: 开始解析数据...')
        # 直接通过json方法返回json字符串或者通过content转码在用json.loads()转化为字符串
        python_obj = response.json()
        result_list = jsonpath(python_obj, '$..result')[0]  # 职位信息结果列表[{}, {}, ...]

        # 如果没有返回值,结束
        if not result_list:
            return True

        # 当没有返回值时,返回的是None
        return result_list

    def save_csv(self, result_list):
        """
        将结果保存为csv文件
        :param result_list: [{}, {}, {}, ...]
        :return:
        """
        csv_file = open('lagou.csv', 'a')

        title_list = result_list[0].keys()  # 获取表头(标题) []

        # 获取表的值数据 [[], [], [], ...]
        values_list = []
        for result_dict in result_list:
            value_list = result_dict.values()
            values_list.append(value_list)

        # 创建csv文件写入对象
        csv_writer = csv.writer(csv_file)

        # 先写入表头字段数据及写入表的值数据
        csv_writer.writerow(title_list)
        for value_list in values_list:
            csv_writer.writerow(value_list)

        # 按照后打开先关闭的原则关闭文件对象
        csv_file.close()

    def run(self):
        while True:
            try:
                response = self.send_request(
                    self.post_url,
                    self.headers,
                    query_dict=self.query_dict,
                    form_dict=self.form_dict
                )
                print('[INFO]: 响应成功')

                result_list = self.parse_page(response)
                if result_list is True:
                    break

                # print(result_list[0], type(result_list[0]))  # TODO: 类型为dict

                self.save_csv(result_list)

            except Exception as e:
                print('[INFO]: {}'.format(e))

            self.page += 1


if __name__ == '__main__':
    LagouSpider().run()
