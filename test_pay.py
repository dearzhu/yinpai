# encoding: utf-8

'''
@author: zhu

@file: test_pay.py

@time: 2018/6/26 10:40

@desc:

'''
# encoding: utf-8

'''
@author: zhu

@file: test1.py

@time: 2018/6/25 14:44

@desc:

'''

import random as rd
import time
import pandas as pd
import numpy as np
import xlrd
import os

count = 500


def get_data():
    # 不符合条件是继续循环
    while True:
        uids_list = []
        date_list = []
        pay_amount_list = []
        date_start = (2018, 7, 1, 0, 0, 0, 0, 0, 0)  # 生成起始的时间元组
        date_end = (2018, 7, 30, 23, 59, 59, 0, 0, 0)  # 生成结束的时间元组
        start = time.mktime(date_start)  # 生成起始的时间戳
        end = time.mktime(date_end)  # 生成结束的时间戳
        count_num = 0
        # 生成随机数
        for i in range(count):
            # 生成uid
            uid = rd.randint(1, 50)
            uids_list.append(uid)
            # 生成日期
            t = rd.randint(start, end)
            date_touple = time.localtime(t)
            date = time.strftime('%Y-%m-%d', date_touple)
            date_list.append(date)
            #生成金额
            amount = rd.randint(10, 200)
            pay_amount_list.append(amount)


            # 转置为矩阵
            data_uid = np.mat(uids_list).T
            data_date = np.mat(date_list).T
            data_amount = np.mat(pay_amount_list).T
            # 拼接矩阵
        data = np.hstack((data_uid, data_date,data_amount))
        data = pd.DataFrame(data, columns=['uid', 'date','pay'])

        data1 = data.groupby(['uid', 'date'],as_index=False).sum()
        print('data1----',data1)
        print('data1----类型',type(data1))

        # 分组
        data2 = data.groupby(['uid']).size()
        print('data1----类型', type(data1))
        data3 = len(data2.index)
        # 统计>7的人数
        for i in data2.index:
            if data2[i] >= 7:
                count_num += 1
            else:
                count_num += 0
        # 计算比例
        bili = count_num / data3
        print('++++++总用户', data3)
        print('老用户数', count_num)
        print('老用户占比', bili)
        # 判断
        if bili >= 0.8 and bili < 1:
            return data
            break

get_data().to_excel('C:\\Users\\anzhi\\Desktop\\sq6.xlsx', 'w++')
