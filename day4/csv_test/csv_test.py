#!-*-coding:utf-8-*-
# !@Date: 2018/11/17 11:40
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
csv模块的相关操作
"""

import csv

# 1.读取csv文件
import json

csv_file = csv.reader(open('names.csv', 'r'))
print(csv_file)
for row in csv_file:
    print(row)
"""
['姓名', '年龄', '性别']
['小刘', '12', '男']
['小黑', '13', '男']
['小白', '14', '男']
['小芳', '15', '女']
"""

# 2.csv文件的写入
title = ['姓名', '年龄', '性别']
person_list = [['小黑黑', '16', '男'], ['小白白', '17', '男'], ['小芳芳', '18', '女']]

csv_writer = csv.writer(open('names2.csv', 'w'))
csv_writer.writerow(title)
for person in person_list:
    csv_writer.writerow(person)


# 3.csv文件写入非标准格式
json_str = '[{"name": "liu", "age": 12, "gender": "male"}, {"name": "liu2", "age": 13, "gender": "male"}]'
python_obj_list = json.loads(json_str)
# print(python_obj, type(python_obj))

title_list = python_obj_list[0].keys()
csv_writer = csv.writer(open('names3.csv', 'w'))
csv_writer.writerow(title_list)

# 先转换为[[], [], ...]格式
values_list = []
for python_obj in python_obj_list:
    value_list = python_obj.values()
    values_list.append(value_list)

for values in values_list:
    csv_writer.writerow(values)
