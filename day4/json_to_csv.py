#!-*-coding:utf-8-*-
# !@Date: 2018/11/16 11:36
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
将json文件转换为csv(逗号分隔值)文件,
csv文件更加便于查看以及可以用excel打开
"""
import json
import csv


def json_to_csv():
    """
    将json文件转换为csv文件
    :return:
    """
    # 获取json文件和csv文件对象
    json_file = open('tencent.json', 'r')
    csv_file = open('tencent.csv', 'w')

    # 将json文件对象加载为python对象
    job_list = json.load(json_file)

    # 获取表头(标题) []
    key_data = job_list[0].keys()
    # 获取表的值数据 [[], [], [], ...]
    value_data = [job.values() for job in job_list]

    # 创建csv文件写入对象
    csv_writer = csv.writer(csv_file)
    # 先写入表头字段数据
    csv_writer.writerow(key_data)
    # 写入表的值数据(注意使用writerows是写入多行数据)
    csv_writer.writerows(value_data)

    # 按照后打开先关闭的原则关闭文件对象
    csv_file.close()
    json_file.close()


if __name__ == '__main__':
    json_to_csv()
