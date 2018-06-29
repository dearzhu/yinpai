# encoding: utf-8

'''
@author: zhu

@file: data_test1.py

@time: 2018/6/25 14:44

@desc:

'''
# !usr/bin/python
import random as rd
import time
import pandas as pd
import numpy as np
import xlrd
import os
import datetime

count = 500


def creat_data():
    uids_list = []
    date_list = []
    pay_amount_list = []
    date_start = (2018, 7, 1, 0, 0, 0, 0, 0, 0)  # 生成起始的时间元组
    date_end = (2018, 7, 30, 23, 59, 59, 0, 0, 0)  # 生成结束的时间元组
    start = time.mktime(date_start)  # 生成起始的时间戳
    end = time.mktime(date_end)  # 生成结束的时间戳
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
        # 生成金额
        amount = rd.randint(20, 300)
        pay_amount_list.append(amount)
    return date_list, pay_amount_list, uids_list


def get_data():
    # 不符合条件是继续循环
    while True:
        old_user_num = 0
        activite_user_num_list = []
        date_list, pay_amount_list, uids_list = creat_data()
        # 转置为矩阵
        data_uid = np.mat(uids_list).T
        data_date = np.mat(date_list).T
        data_amount = np.mat(pay_amount_list).T
        # 拼接矩阵
        data = np.hstack((data_uid, data_date, data_amount))
        data = pd.DataFrame(data, columns=['uid', 'date', 'pay'])
        # 将pay(object) 转换成int
        data['pay'] = pd.DataFrame(data['pay'], dtype=np.int)
        # 按照uid date 分组
        data = data.groupby(['uid', 'date'], as_index=False).sum()


        data1 = data.loc[:, ['uid', 'date']]
        # print(data1)
        data1 = np.array(data1)
        result_dict = {}
        # 去重，根据uid建立字典，
        date_set = list(set([i[0] for i in data1]))
        for i in date_set:
            result_dict[i] = []
        for i in data1:
            result_dict[i[0]].append(i[1])
        # print(result_dict)
        # 分组，获取每一组的人数个数
        data2 = data.groupby(['uid']).size()

        # print('data2------',type(data2))
        # 获取总用户人数
        user_num = len(data2.index)
        # 按照uid进行透视，统计金额
        data4 = pd.pivot_table(data, index=['uid'], values=['pay'], aggfunc=sum)
        # 将dataframe转换成dict,将金额和uid 修改为字典， 判断老用户的金额
        data5 = data4.to_dict()
        # print('data5------------',data5)
        # 统计>7的人数,按照uid对老用户金额进行限制
        for i in data2.index:
            # 获取对应用户的付款时间
            data_key = result_dict[i]
            # 遍历对应的时间
            for j in range(len(data_key)):
                # 求活跃用户，七天内至少有2次登录
                if (string_toDatetime(data_key[j]) - string_toDatetime(data_key[j - 1])).days <= 6:
                    # 将毁约用户添加到list,目的统计活跃用户个数
                    activite_user_num_list.append(i)
            # 老用户30天登录7次 且金额为1000~3000
            if data2[i] >= 7 and data5['pay'][i] > 1000 and data5['pay'][i] < 3000:
                old_user_num += 1
            else:
                old_user_num += 0
        # 计算比例
        active_user_num = len(list(set(activite_user_num_list)))
        # 活跃用户比例
        active_user_percentage = active_user_num / user_num
        # 老用户比例
        old_user_percentage = old_user_num / user_num
        print('总用户', user_num)
        print('老用户数', old_user_num)
        print('活跃用户人数',active_user_num)
        print('老用户占比', old_user_percentage)
        print('活跃用户占比', active_user_percentage)
        # 判断  新老用户的比例都在1.8~0.1之间
        if old_user_percentage >= 0.8 and old_user_percentage < 1 and active_user_percentage >= 0.8 and active_user_percentage <= 1:
            # print(data)
            return data
            break


# 字符串时间格式转换为日期格式
def string_toDatetime(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d")


get_data().to_excel('C:\\Users\\anzhi\\Desktop\\sq6.xlsx', 'w++')
