#!/usr/bin/env python
# encoding: utf-8
'''
@author: Zake Yao
@account: syao
@license: (C) Copyright 2015-2019, Media Experience Lab.
@contact: yaoshunyu96@gmail.com
@file: testteacher
@time: 2019-05-09 14:51
@desc:
この.pyの実行はpython3 testteacher.py　でいいです
これがメインのプログラムで
これだけ実行したらいいです
delの結果を基準として見てください
delがないのは、長いパターンは短いを含んでいる
Correct score_del　は　１　の時は正解、０は間違い
以上
'''
__author__ = 'Zake Yao'

import os
import csv
import sys
# import pysnooper
import json
import string
from main.pattern_fineder import PatternFinder
import main.tools
from fuzzywuzzy import fuzz
from main.teacher import Teacher
from main.teacher import NewTeacher
from main.teacher import ProTeacher


# This is the teacher who is going to be tested
class TestTeacher(object):
    """docstring for TestTeacher"""

    def __init__(self, name, test_csvpath):
        super(TestTeacher, self).__init__()
        self.name = name
        self.dic_com_ori = {}  # 压缩后下标：占了几个frame，注意补上被省略的,由于还原真正错的地方是哪一个帧数 #每个动作占了几帧可以发现
        self.test_csvpath = test_csvpath
        # for proteacher data to calculate the score 分别是test做出老手老师的各个pattern的次数，和每种长度pattern的数量，下面是新手的
        self.score_keeper_pro = {}
        self.class_keeper_pro = {}
        # for newteacher data to calculate the score
        self.score_keeper_new = {}
        self.class_keeper_new = {}
        self.ac_list_com = []  # 压缩后的list
        self.ac_list_ori = []  # 原始的list

        self.dic_action_wrong = {}  # 这里记录的只是 动作数：错的是啥，但是可以和dic_com_ori一起还原出哪里错了
        self.dic_action_right = {} # TODO(Zake Yao)这里好像没用，把没用的成员变量删了;
        self.dic_action_change = {}   #we want to change to wrong pt to the right pt ,this dic is to change the wrong dic

        # use to keep the json data
        # first is the pro patterns
        self.pf_temp_saver_pro_2 = {}
        self.pf_temp_saver_pro_3 = {}
        self.pf_temp_saver_pro_4 = {}
        self.pf_temp_saver_pro_5 = {}
        self.pf_temp_saver_pro_6 = {}
        self.pf_temp_saver_pro_7 = {}
        self.pf_temp_saver_pro_8 = {}
        self.pf_temp_saver_pro_9 = {}
        self.pf_temp_saver_pro_10 = {}
        # second is the new patterns
        self.pf_temp_saver_new_2 = {}
        self.pf_temp_saver_new_3 = {}
        self.pf_temp_saver_new_4 = {}
        self.pf_temp_saver_new_5 = {}
        self.pf_temp_saver_new_6 = {}
        self.pf_temp_saver_new_7 = {}
        self.pf_temp_saver_new_8 = {}
        self.pf_temp_saver_new_9 = {}
        self.pf_temp_saver_new_10 = {}

        csv_file = csv.reader(open(test_csvpath))  # use to read the test date
        for item in csv_file:
            self.ac_list_ori.append(item[0])

    # use to change the action list into ID
    # return the ID of the action list for pattern
    def IDgeter_t(self, list_ac_k):
        temp_str = ""
        for index in range(len(list_ac_k)):
            temp_1 = list_ac_k[index]
            f = open("/Users/syao/desktop/res/label_name.txt", "r")
            for temp_item in f.readlines():
                temp_item = temp_item.strip('\n')
                sp_temp_item = temp_item.split(",")
                if (temp_1 == sp_temp_item[0]):
                    temp_str += sp_temp_item[2]
                # print(sp_temp_item[2])
            f.close()
        return temp_str

    # use to get the single ID for one action
    def IDgeterforsingel_t(self, str_ac):
        f = open("/Users/syao/desktop/res/label_name.txt", "r")
        temp_str = ""
        for temp_item in f.readlines():
            temp_item = temp_item.strip('\n')
            sp_temp_item = temp_item.split(",")
            if str_ac == sp_temp_item[0]:
                temp_str = sp_temp_item[2]
                break
        f.close()
        return temp_str
    # use to get the real action name of the action form the ID
    # it is the reverse function  to the IDgerter_t
    def actiongeter_t(self, list_ac_k):
        temp_list = []
        for index in range(len(list_ac_k)):
            temp_1 = list_ac_k[index]
            f = open("/Users/syao/desktop/res/label_name.txt", "r")
            for temp_item in f.readlines():
                temp_item = temp_item.strip('\n')
                sp_temp_item = temp_item.split(",")
                if (temp_1 == sp_temp_item[2]):
                    temp_list.append(sp_temp_item[0])
                # print(sp_temp_item[2])
            f.close()
        return temp_list


    # use to read the data that save the pattern in json
    # than return the dic of the json
    # span use to chose the which pf
    # use which_teacher to get the data is from proteacher or newteacher
    # 1 for proteacher,0 for newteacher
    def jsonReader_pf(self, json_path, span, which_teacher):
        with open(json_path, 'r')as f:
            json_file = json.load(f)
        if which_teacher == 1:
            if span == 2:  # 这里是融合才能把数据都添加进去
                self.pf_temp_saver_pro_2 = self.dicMerger(self.pf_temp_saver_pro_2.copy(), json_file.copy())
            elif span == 3:
                self.pf_temp_saver_pro_3 = self.dicMerger(self.pf_temp_saver_pro_3.copy(), json_file.copy())
            elif span == 4:
                self.pf_temp_saver_pro_4 = self.dicMerger(self.pf_temp_saver_pro_4.copy(), json_file.copy())
            elif span == 5:
                self.pf_temp_saver_pro_5 = self.dicMerger(self.pf_temp_saver_pro_5.copy(), json_file.copy())
            elif span == 6:
                self.pf_temp_saver_pro_6 = self.dicMerger(self.pf_temp_saver_pro_6.copy(), json_file.copy())# GAI
            elif span == 7:
                self.pf_temp_saver_pro_7 = self.dicMerger(self.pf_temp_saver_pro_7.copy(), json_file.copy())
            elif span == 8:
                self.pf_temp_saver_pro_8 = self.dicMerger(self.pf_temp_saver_pro_8.copy(), json_file.copy())
            elif span == 9:
                self.pf_temp_saver_pro_9 = self.dicMerger(self.pf_temp_saver_pro_9.copy(), json_file.copy())
            elif span == 10:
                self.pf_temp_saver_pro_10 = self.dicMerger(self.pf_temp_saver_pro_10.copy(), json_file.copy())

        elif which_teacher == 0:
            if span == 2:
                self.pf_temp_saver_new_2 = self.dicMerger(self.pf_temp_saver_new_2.copy(), json_file.copy())
            elif span == 3:
                self.pf_temp_saver_new_3 = self.dicMerger(self.pf_temp_saver_new_3.copy(), json_file.copy())
            elif span == 4:
                self.pf_temp_saver_new_4 = self.dicMerger(self.pf_temp_saver_new_4.copy(), json_file.copy())
            elif span == 5:
                self.pf_temp_saver_new_5 = self.dicMerger(self.pf_temp_saver_new_5.copy(), json_file.copy())
            elif span == 6:
                self.pf_temp_saver_new_6 = self.dicMerger(self.pf_temp_saver_new_6.copy(), json_file.copy())# GA
            elif span == 7:
                self.pf_temp_saver_new_7 = self.dicMerger(self.pf_temp_saver_new_7.copy(), json_file.copy())
            elif span == 8:
                self.pf_temp_saver_new_8 = self.dicMerger(self.pf_temp_saver_new_8.copy(), json_file.copy())
            elif span == 9:
                self.pf_temp_saver_new_9 = self.dicMerger(self.pf_temp_saver_new_9.copy(), json_file.copy())
            elif span == 10:
                self.pf_temp_saver_new_10 = self.dicMerger(self.pf_temp_saver_new_10.copy(), json_file.copy())
    # use read the pf in one time
    def jsonReader_pf_onetime(self, json_path, name, which_teacher):
        for x in range(2,11):
            path_final = os.path.join(json_path,name,str(x)+".json")
            self.jsonReader_pf(path_final, x, which_teacher)

    # use to update the dic
    # when the key is existed,add 1 to the value
    # or add one to the dic
    def dicMerger(self, dict_1, dict_2):  # 有相同的的就加新的值，没有就创建
        for item in dict_2:
            if item in dict_1:
                dict_1[item] += dict_2[item]  # add another value
            else:
                dict_1[item] = dict_2[item]
        return dict_1

    # use to delete the data in both dic
    # left the data witch for only It's own side
    # return 2 dics without common pattern
    def dicCommonDeleter(self, dict_1, dict_2):
        dict_1_temp = dict_1.copy()
        dict_2_temp = dict_2.copy()
        set_common = dict_1.keys() & dict_2.keys()  # set
        for item in set_common:
            dict_1_temp.pop(item)
            dict_2_temp.pop(item)
        return dict_1_temp, dict_2_temp

    # use delete the common data in one time
    def dicCommonDeleteOnetime(self):
        self.pf_temp_saver_pro_2, self.pf_temp_saver_new_2 = self.dicCommonDeleter(self.pf_temp_saver_pro_2,
                                                                                   self.pf_temp_saver_new_2)

        self.pf_temp_saver_pro_3, self.pf_temp_saver_new_3 = self.dicCommonDeleter(self.pf_temp_saver_pro_3,
                                                                                   self.pf_temp_saver_new_3)

        self.pf_temp_saver_pro_4, self.pf_temp_saver_new_4 = self.dicCommonDeleter(self.pf_temp_saver_pro_4,
                                                                                   self.pf_temp_saver_new_4)
        self.pf_temp_saver_pro_5, self.pf_temp_saver_new_5 = self.dicCommonDeleter(self.pf_temp_saver_pro_5,
                                                                                   self.pf_temp_saver_new_5)
        self.pf_temp_saver_pro_6, self.pf_temp_saver_new_6 = self.dicCommonDeleter(self.pf_temp_saver_pro_6,
                                                                                   self.pf_temp_saver_new_6)
        self.pf_temp_saver_pro_7, self.pf_temp_saver_new_7 = self.dicCommonDeleter(self.pf_temp_saver_pro_7,
                                                                                   self.pf_temp_saver_new_7)
        self.pf_temp_saver_pro_8, self.pf_temp_saver_new_8 = self.dicCommonDeleter(self.pf_temp_saver_pro_8,
                                                                                   self.pf_temp_saver_new_8)
        self.pf_temp_saver_pro_9, self.pf_temp_saver_new_9 = self.dicCommonDeleter(self.pf_temp_saver_pro_9,
                                                                                   self.pf_temp_saver_new_9)
        self.pf_temp_saver_pro_10, self.pf_temp_saver_new_10 = self.dicCommonDeleter(self.pf_temp_saver_pro_10,
                                                                                   self.pf_temp_saver_new_10)

    # use to show the common pattern in the dic
    # return the same keys in a list
    def dicCommonShower(self, dict_1, dict_2):
        set_common = dict_1.keys() & dict_2.keys()  # set include the same keys in the dic
        return set_common

    def dicCommenShowerOnetime(self):
        print(self.dicCommonShower(self.pf_temp_saver_pro_2.copy(), self.pf_temp_saver_new_2.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_3.copy(), self.pf_temp_saver_new_3.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_4.copy(), self.pf_temp_saver_new_4.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_5.copy(), self.pf_temp_saver_new_5.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_6.copy(), self.pf_temp_saver_new_6.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_7.copy(), self.pf_temp_saver_new_7.copy()))
        print(self.dicCommonShower(self.pf_temp_saver_pro_8.copy(), self.pf_temp_saver_new_8.copy()))
        #v2 use to show the times
    def dicCommenShowerOnetime_v2(self):
        temp2 = self.dicMerger(self.pf_temp_saver_pro_2.copy(), self.pf_temp_saver_new_2.copy())
        temp3 = self.dicMerger(self.pf_temp_saver_pro_3.copy(), self.pf_temp_saver_new_3.copy())
        temp4 = self.dicMerger(self.pf_temp_saver_pro_4.copy(), self.pf_temp_saver_new_4.copy())
        temp5 = self.dicMerger(self.pf_temp_saver_pro_5.copy(), self.pf_temp_saver_new_5.copy())
        temp6 = self.dicMerger(self.pf_temp_saver_pro_6.copy(), self.pf_temp_saver_new_6.copy())
        temp7 = self.dicMerger(self.pf_temp_saver_pro_7.copy(), self.pf_temp_saver_new_7.copy())
        temp8 = self.dicMerger(self.pf_temp_saver_pro_8.copy(), self.pf_temp_saver_new_8.copy())
        temp2 = self.dicMerger(temp2, temp3)
        temp4 = self.dicMerger(temp4, temp5)
        temp6 = self.dicMerger(temp6, temp7)
        temp8 = self.dicMerger(temp8, temp2)
        temp4 = self.dicMerger(temp4, temp6)
        temp8 = self.dicMerger(temp8,temp4)
        return main.tools.order_dic_val(temp8)
        # v3 use to show the times，and del the include situation
    def dicCommenShowerOnetime_v3(self):
        temp2 = self.dicMerger(self.pf_temp_saver_pro_2, self.pf_temp_saver_new_2)
        temp3 = self.dicMerger(self.pf_temp_saver_pro_3, self.pf_temp_saver_new_3)
        temp4 = self.dicMerger(self.pf_temp_saver_pro_4, self.pf_temp_saver_new_4)
        temp5 = self.dicMerger(self.pf_temp_saver_pro_5, self.pf_temp_saver_new_5)
        temp6 = self.dicMerger(self.pf_temp_saver_pro_6, self.pf_temp_saver_new_6)
        temp7 = self.dicMerger(self.pf_temp_saver_pro_7, self.pf_temp_saver_new_7)
        temp8 = self.dicMerger(self.pf_temp_saver_pro_8, self.pf_temp_saver_new_8)
        temp2 = self.dicMerger(temp2, temp3)
        temp4 = self.dicMerger(temp4, temp5)
        temp6 = self.dicMerger(temp6, temp7)
        temp8 = self.dicMerger(temp8, temp2)
        temp4 = self.dicMerger(temp4, temp6)
        temp8 = self.dicMerger(temp8,temp4)
        return main.tools.order_dic_val(main.tools.shortptdeleter_rel(temp8))


    # read csv and use list to save it
    # reflesh the list to the new csv
    def csvReader_t(self):  # default path is in the object
        csv_file = csv.reader(open(self.test_csvpath))
        listoftemp = []
        for item in csv_file:
            # print type(item[0])
            listoftemp.append(item[0])
        if len(listoftemp) == 0:
            print("Error!Path maybe null")
        self.ac_list_ori.clear()
        self.ac_list_ori += listoftemp

    # TODO(Zake Yao): rewrite this function with the regular pattercleaner in father class
    # use to clear the dic to delete if the time is less than some value
    # use class_keeper_XXX and score_keeper_XXX's data
    # if only few times in the class_keeper_XXX, than delete it both in the two dic
    # at least the times need to be more than show_times eg.show_times:1 it will be deleted which the times is 1
    def patterncleanerfortesttea(self, show_times):  # show_times 是要删除次数的最大值
        temp_class_keeper_pro = self.class_keeper_pro.copy()
        temp_score_keeper_pro = self.score_keeper_pro.copy()
        temp_class_keeper_new = self.class_keeper_new.copy()
        temp_score_keeper_new = self.score_keeper_new.copy()

        for key in self.class_keeper_pro:
            if (temp_class_keeper_pro[key]) <= show_times:
                if temp_score_keeper_pro[len(key)] < 1:
                    print("Error! The times in score is less 1,and you can't minus 1")
                if temp_score_keeper_pro[len(key)] == 1:
                    temp_score_keeper_pro.pop(len(key))
                    temp_class_keeper_pro.pop(key)
                else:
                    temp_score_keeper_pro[len(key)] -= 1  # minus 1 in the score_keeper_pro
                    temp_class_keeper_pro.pop(key)

        for key in self.class_keeper_new:
            if (temp_class_keeper_new[key]) <= show_times:
                if temp_score_keeper_new[len(key)] < 1:
                    print("Error! The times in score is less 1,and you can't minus 1")  # 如果下面的删除放在前面则会在这个的len处出错
                if temp_score_keeper_new[len(key)] == 1:
                    temp_score_keeper_new.pop(len(key))
                    temp_class_keeper_new.pop(key)
                else:
                    temp_score_keeper_new[len(key)] -= 1  # minus 1 in the score_keeper_new
                    temp_class_keeper_new.pop(key)

        self.class_keeper_pro = temp_class_keeper_pro.copy()
        self.score_keeper_pro = temp_score_keeper_pro.copy()
        self.class_keeper_new = temp_class_keeper_new.copy()
        self.score_keeper_new = temp_score_keeper_new.copy()

    # use to find the pattern for this teacher
    # to see when the tester do the wrong pattern
    # to sum how many right pattern tester has down and how many times each action pattern have been done
    # save the pattern and which frame, another function will deal with it to find the better choice
    # @pysnooper.snoop()

    def patternCheeker(self,flagofptlength):  # 只运行一次，再运行会刷新dict的，flagofptlength用来定义最长的pattern数
        # 统计每种出现了多少次
        flagconunt = 0
        pattern_temp = []
        temp_score_keeper_pro = {}
        temp_class_keeper_pro = {}
        temp_score_keeper_new = {}
        temp_class_keeper_new = {}
        for item in range(len(self.ac_list_com)): # 查看list里面全部的元素
            for x in range(flagofptlength):
                if item + x < len(self.ac_list_com):
                    pattern_temp.append(self.ac_list_com[item + x])  # 这里把一个个的字符分开了，所以下面的len对于一个list来说就是这个pattern的长度
                    if len(pattern_temp) == 2:  # 这里还需要更大的判断来判别是符合加分还是减分的字典了
                        pattern_str = (''.join(pattern_temp))#把分开的合在一起了
                        if pattern_str in self.pf_temp_saver_pro_2:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:  # if the new one is already in
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1

                            if 2 in temp_score_keeper_pro:  #
                                temp_score_keeper_pro[2] += 1
                            else:
                                temp_score_keeper_pro[2] = 1

                        elif pattern_str in self.pf_temp_saver_new_2:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str  # the dic is to save the wrong pattern
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 2 in temp_score_keeper_new:
                                temp_score_keeper_new[2] += 1
                            else:
                                temp_score_keeper_new[2] = 1
                    elif len(pattern_temp) == 3:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_3:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 3 in temp_score_keeper_pro:
                                temp_score_keeper_pro[3] += 1
                            else:
                                temp_score_keeper_pro[3] = 1
                        elif pattern_str in self.pf_temp_saver_new_3:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 3 in temp_score_keeper_new:
                                temp_score_keeper_new[3] += 1
                            else:
                                temp_score_keeper_new[3] = 1

                    elif len(pattern_temp) == 4:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_4:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 4 in temp_score_keeper_pro:
                                temp_score_keeper_pro[4] += 1
                            else:
                                temp_score_keeper_pro[4] = 1
                        elif pattern_str in self.pf_temp_saver_new_4:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 4 in temp_score_keeper_new:
                                temp_score_keeper_new[4] += 1
                            else:
                                temp_score_keeper_new[4] = 1
                    elif len(pattern_temp) == 5:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_5:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 5 in temp_score_keeper_pro:
                                temp_score_keeper_pro[5] += 1
                            else:
                                temp_score_keeper_pro[5] = 1
                        elif pattern_str in self.pf_temp_saver_new_5:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 5 in temp_score_keeper_new:
                                temp_score_keeper_new[5] += 1
                            else:
                                temp_score_keeper_new[5] = 1
                    elif len(pattern_temp) == 6:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_6:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 6 in temp_score_keeper_pro:
                                temp_score_keeper_pro[6] += 1
                            else:
                                temp_score_keeper_pro[6] = 1
                        elif pattern_str in self.pf_temp_saver_new_6:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 6 in temp_score_keeper_new:
                                temp_score_keeper_new[6] += 1
                            else:
                                temp_score_keeper_new[6] = 1
                    elif len(pattern_temp) == 7:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_7:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 7 in temp_score_keeper_pro:
                                temp_score_keeper_pro[7] += 1
                            else:
                                temp_score_keeper_pro[7] = 1
                        elif pattern_str in self.pf_temp_saver_new_7:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 7 in temp_score_keeper_new:
                                temp_score_keeper_new[7] += 1
                            else:
                                temp_score_keeper_new[7] = 1
                    elif len(pattern_temp) == 8:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_8:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 8 in temp_score_keeper_pro:
                                temp_score_keeper_pro[8] += 1
                            else:
                                temp_score_keeper_pro[8] = 1
                        elif pattern_str in self.pf_temp_saver_new_8:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 8 in temp_score_keeper_new:
                                temp_score_keeper_new[8] += 1
                            else:
                                temp_score_keeper_new[8] = 1



                    # #---------------------------------可能用不到下面的了---------------------------------
                    elif len(pattern_temp) == 9:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_9:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 9 in temp_score_keeper_pro:
                                temp_score_keeper_pro[9] += 1
                            else:
                                temp_score_keeper_pro[9] = 1
                        elif pattern_str in self.pf_temp_saver_new_9:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 9 in temp_score_keeper_new:
                                temp_score_keeper_new[9] += 1
                            else:
                                temp_score_keeper_new[9] = 1
                    elif len(pattern_temp) == 10:
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_10:
                            self.dic_action_right[item] = pattern_str  # the dic is to save the right pattern
                            if pattern_str in temp_class_keeper_pro:
                                temp_class_keeper_pro[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_pro[pattern_str] = 1
                            if 10 in temp_score_keeper_pro:
                                temp_score_keeper_pro[10] += 1
                            else:
                                temp_score_keeper_pro[10] = 1
                        elif pattern_str in self.pf_temp_saver_new_10:
                            # Here to know the pattern is in the new group
                            self.dic_action_wrong[item] = pattern_str
                            if pattern_str in temp_class_keeper_new:
                                temp_class_keeper_new[pattern_str] += 1  # 添加一个字典用来记录每个种类的出现了几次
                            else:
                                temp_class_keeper_new[pattern_str] = 1
                            if 10 in temp_score_keeper_new:
                                temp_score_keeper_new[10] += 1
                            else:
                                temp_score_keeper_new[10] = 1

            pattern_temp.clear()  # clear the list for new pattern to cheek
        self.score_keeper_pro = temp_score_keeper_pro.copy()
        self.class_keeper_pro = temp_class_keeper_pro.copy()
        self.score_keeper_new = temp_score_keeper_new.copy()
        self.class_keeper_new = temp_class_keeper_new.copy()

    # use to forecast the next action witch one is best
    # input the pattern of now and return the best next action
    # if no next patern in the dic return ""
    # 用于预测是否有更好的下一个动作的预测系统，现在只是通过对不同的长度的pt库里面看有没有刚好可以修改的
    def patternForecaster(self, pattern_temp, maxlen):  # TODO(Zake Yao):需不需要添加一个flag用来判断有没有清楚共通的部分
        if len(pattern_temp) > maxlen:
            print("Error! The length of the pattern can't longer than "+str(maxlen)+".")
            sys.exit(1)
        if len(pattern_temp) < 1:
            print("Error! The length of the pattern can't shorter than 1.")
            sys.exit(1)
        if len(pattern_temp) == 2:  # cheek the length and return the frequency of the max one
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_2:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (1/2.0):#都看只差一个的时候
                    if self.pf_temp_saver_pro_2[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_2[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 3:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_3:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (2/3.0):
                    if self.pf_temp_saver_pro_3[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_3[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 4:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_4:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (3/4.0):
                    if self.pf_temp_saver_pro_4[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_4[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 5:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_5:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (4/5.0):
                    if self.pf_temp_saver_pro_5[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_5[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 6:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_6:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (5/6.0):
                    if self.pf_temp_saver_pro_6[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_6[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 7:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_7:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (6/7.0):
                    if self.pf_temp_saver_pro_7[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_7[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 8:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_8:
                if (fuzz.ratio(item, pattern_temp)/100.0) > (7/8.0):
                    if self.pf_temp_saver_pro_8[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_8[item]
                        max_temp_item = item
            return max_temp_item


    # use to change the wrong pattern to the right pattern
    # by cheek the first some action of the pattern to use the function patternForecaster to get the right action
    # 这个是用来吧错的list里面的动作进行修改，如果老手的数据里面有对应的就可以输出到right的数组里
    # maxlen will change with the patterncheeker function parameter
    def dicPatternReviser(self,maxlen):  # 如果是这个动作老手里面没有对应的修改怎么办
        for item in self.dic_action_wrong:
            if len(self.dic_action_wrong[item]) < 1:
                print("Error!It must be longer than 1 in the wrong action list")
                sys.exit(1)
            if len(self.dic_action_wrong[item]) > maxlen:
                print("Error!It must be shorter than "+str(maxlen)+"in the wrong action list")
                sys.exit(1)
            # It will cheek the length auto automatically
            self.dic_action_change[item] = self.patternForecaster(str(self.dic_action_wrong[item]),maxlen)

    # use to get frame instead of action number in the dic
    # to rewrite the dic，return a new dic with frame
    # also assign the dic_action_wrong_fra to save the value
    def dicFramegeter(self, dic_temp):
        new_dic = {}
        for item in dic_temp:
            sum_temp = 0
            for x in self.dic_com_ori:
                # cheek
                #sum_temp += self.dic_com_ori[x]  # 这个是在之后显示
                if (item == x):
                    new_dic[sum_temp] = dic_temp[item]
                    break
                # then add
                sum_temp += self.dic_com_ori[x]#
        # self.dic_action_wrong_fra = new_dic.copy()
        return new_dic
    # change the last function to deal with list
    def dicFramegeter4list(self, list_temp):
        new_dic = {}
        for item in range(len(list_temp)):
            sum_temp = 0
            for x in self.dic_com_ori:
                # cheek
                #这个是在之后显示
                #sum_temp += self.dic_com_ori[x]  # 这个的位置将会决定，是做完这个pattern再显示，还是做这个pt前显示
                if (item == x):
                    new_dic[sum_temp] = list_temp[item]
                    break
                # then add
                sum_temp += self.dic_com_ori[x] #这个的位置将会决定，是做完这个pattern再显示，还是做这个pt前显示
        # self.dic_action_wrong_fra = new_dic.copy()
        return new_dic

    # use to find the patterns that have displayed in the test teacher
    # 因为不是需要提前处理的所以不用必须储存
    def testpfFinder(self, show_times):
        '''
        :param show_times:if "show_times" is not 0 ,it will delete the few times patterns in set
        :return:the pattern dic of test
        '''
        temp_obj = PatternFinder(2, self.test_csvpath)
        temp_obj2 = PatternFinder(3, self.test_csvpath)
        temp_dic = self.dicMerger(temp_obj.dictemper, temp_obj2.dictemper)
        temp_obj = PatternFinder(4, self.test_csvpath)
        temp_obj2 = PatternFinder(5, self.test_csvpath)
        temp_dic_2 = self.dicMerger(temp_obj.dictemper, temp_obj2.dictemper)
        temp_dic = self.dicMerger(temp_dic, temp_dic_2)
        temp_obj2 = PatternFinder(6, self.test_csvpath)
        temp_dic = self.dicMerger(temp_dic, temp_obj2.dictemper)
        # than delete the pattern less than 2
        if show_times != 0:
            temp_dic = main.tools.patterncleaner(temp_dic, show_times)

        return temp_dic

    # use to compress the list to the ID
    # and build the dic to contact the 2 list
    # return the list of the action list
    def compressList_id_t(self, list_ac, a, b):  #
        counter_ac = 0
        counter_recover = 0 # 记住被删除的多少个结果的大小
        temp_ac = ""
        temp_ac_list = []
        for x in list_ac:  # 没有加上最后一次
            if temp_ac == "":  # to evaluate the initial value
                temp_ac = x.encode('utf-8').decode('utf-8-sig').strip()
                counter_ac = 1  # first time
                continue
            # 如果不是初始值
            elif temp_ac!= x.encode('utf-8').decode('utf-8-sig').strip():  # see the next is different 如果不同的话，结算当前的
                if counter_ac < a:  # 如果结算的时候少于a
                    counter_recover += counter_ac  # 这个补上了count了几次的
                    temp_ac = x.encode('utf-8').decode('utf-8-sig').strip()#切换当前动作到x
                    counter_ac =1
                    # if (counter_recover > 9):
                    #     print("Attention:Maybe error.It's hard for counter_recover to be over than 9!")TODO(Zake Yao):这个是干嘛的我忘了，你等会记得看看
                    #     print(counter_recover)
                    continue  # 因为使用了continue所以跳过了后面对counter的清空
                elif counter_ac <= b:#如果在a到b的范围内的话
                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))  # add the last one
                    self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover
                elif counter_ac > b:  # 要是大于b的时候
                    temp_conter_acs = counter_ac // b  # conclute how many times
                    for item in range(temp_conter_acs):
                        temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                        self.dic_com_ori[len(temp_ac_list) - 1] = b  ##
                    self.dic_com_ori[len(temp_ac_list) -1] += counter_ac % b + counter_recover  ##
                # 这个是每个下标和和原本对于的frame数
                # 基础的4个加上多于被省略，是4个是因为b是4
                # 包括取余省略的和小于2省略的
                temp_ac = x.encode('utf-8').decode('utf-8-sig').strip()
                counter_ac = 1
                counter_recover = 0  # reflash
            else:#还是一样的话只是加一，给计数器
                counter_ac += 1
        # 这个是对最后剩余的处理
        if counter_ac >= a:  # use to add the last element# 最后一个元素如果是1的时候，给最后一个元素加一
            if counter_ac <= b:
                temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover
            else:
                temp_conter_acs = counter_ac // b  # conclute how many times
                for item in range(temp_conter_acs):
                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                    self.dic_com_ori[len(temp_ac_list) - 1] = b
                self.dic_com_ori[len(temp_ac_list) - 1] = b + counter_ac % b + counter_recover
        else:
            temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
            self.dic_com_ori[len(temp_ac_list) - 1]=  counter_recover +1
        # if (len(self.dic_com_ori) - len(self.ac_list_ori)) < a:  # when the last one is 1
        #     self.dic_com_ori[len(temp_ac_list) - 1] += a - 1

        self.ac_list_com.clear()
        self.ac_list_com += temp_ac_list
        return temp_ac_list

    # use to merge all the Pro teacher dic
    def dicMergerforPro(self, show_times):  # 融合了全部的老手老师的数据
        temp_dic = {}
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_2)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_3)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_4)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_5)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_6)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_7)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_8)
        # temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_9)
        # temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_pro_10)

        if show_times != 0:
            temp_dic = main.tools.patterncleaner(temp_dic, show_times)
        return temp_dic

    # use to merge all the New teacher dic
    def dicMergerforNew(self, show_times):  # 融合了全部的新手老师的数据
        temp_dic = {}
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_2)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_3)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_4)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_5)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_6)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_7)
        temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_8)
        # temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_9)
        # temp_dic = self.dicMerger(temp_dic, self.pf_temp_saver_new_10)
        if show_times != 0:
            temp_dic = main.tools.patterncleaner(temp_dic, show_times)
        return temp_dic

    # use to get the score from the data
    # version : to use the jaccard distance
    def scorecalculater_jd(self, show_times):
        set_test = self.testpfFinder(show_times)  # delete the patterns witch only show once
        set_datapro = self.dicMergerforPro(show_times)
        set_datanew = self.dicMergerforNew(show_times)
        dis_1 = self.jaccard_dist(set_test.keys(), set_datapro.keys())
        dis_2 = self.jaccard_dist(set_test.keys(), set_datanew.keys())
        # 大于0.5偏向pro，小于0.5偏向new
        dis = 1.0 - (dis_1 / (dis_1 + dis_2))  # Maybe need another　Equation
        return dis

    # use to build a list of teacher objects
    # all的data存在一个文件夹里
    # to this function to calculate the tfidf
    def teacherlist(self, in_path):  # 这个结构可以是 name ： dic
        # eg.{name1:{pt1:sum_num,pt2:sum_num,...}, name2:{...}...}
        # TODO（Zake Yao）: to prevent that two objs has the same name
        # 读取数据
        dict_temp = {}
        json_files = os.listdir(in_path)
        for file in json_files:
            # 从文件名里面分割出名称
            temp_name_1 = file.split(".")
            temp_name_2 = temp_name_1[0].split("_")
            if temp_name_2[1] == "all" and temp_name_2[0] not in dict_temp:
                with open(in_path + file, 'r')as f:
                    json_read = json.load(f)
                    dict_temp[temp_name_2[0]] = json_read  # 放到一个大的字典里

        return dict_temp  # 然后返回这个字典

    # use to get the score from the data
    # to use the TF-IDF
    def scorecalculater_TF(self):
        pass

    # use to get the score from the data
    # version : to use the DP matching
    def scorecalculater_dp(self):
        pass
    #use the average score and sum the matching times to get the score
    def scorecalculater_ave(self):
        # 引入
        # 让程序在外层删除吧,记住删除程序在外层
        # 先看在不在，有没有数据
        sum_new = 0
        sum_pro = 0
        for x in range(2, 11):
            if x in self.score_keeper_new:
                sum_new += self.score_keeper_new[x]

        for x in range(2, 11):
            if x in self.score_keeper_pro:
                sum_pro += self.score_keeper_pro[x]

        # 然后计算
        score = 0
        if sum_new!=0 or sum_pro!=0:
            score = (sum_pro/(sum_pro+sum_new)-sum_new/(sum_pro+sum_new))*50+50  # 如果两个都不为0
            # print(score)
        else:
            score = 50 #两个都为空的时候，会变成50分
        return score

    # jaccard distance
    def jaccard_dist(self, tp, tq):  # 这种方法没有考虑元素的重复性吧
        '''
        计算两个向量的杰卡德距离
        INPUT  -> 长度一致的向量1、向量2
        '''
        set_p = set(tp)
        set_q = set(tq)
        dis: float = float(len((set_p | set_q) - (set_p & set_q))) / len(set_p | set_q)
        # dis = pdist([p, q],'jaccard')
        return dis
    # use to delete the pattern when in the situation that have longer pattern include the shorter ones
    # this function will change the value of score_keeper and class_keeper, so it have to be the member function
    def shortptdeleter(self):
        temp_class_keeper_pro = self.class_keeper_pro.copy()
        temp_score_keeper_pro = self.score_keeper_pro.copy()
        temp_class_keeper_new = self.class_keeper_new.copy()
        temp_score_keeper_new = self.score_keeper_new.copy()

        for x in self.class_keeper_pro:
            if x[0:-1] in temp_class_keeper_pro:
                (temp_class_keeper_pro,temp_score_keeper_pro) = self.eachsmallpt(x,temp_class_keeper_pro,temp_score_keeper_pro)
        for x in self.class_keeper_new:
            if x[0:-1] in temp_class_keeper_new:
                (temp_class_keeper_new,temp_score_keeper_new) = self.eachsmallpt(x,temp_class_keeper_new,temp_score_keeper_new)
        self.class_keeper_pro = temp_class_keeper_pro.copy()
        self.score_keeper_pro = temp_score_keeper_pro.copy()
        self.class_keeper_new = temp_class_keeper_new.copy()
        self.score_keeper_new = temp_score_keeper_new.copy()

    def eachsmallpt(self,key_t,dic_class,dic_score):
        dic_class_t = dic_class.copy()
        dic_score_t = dic_score.copy()

        if key_t[0:-1] in dic_class:
            (dic_class_t, dic_score_t) = self.eachsmallpt(key_t[0:-1],dic_class_t,dic_score_t)
        else:
            if dic_score[len(key_t)] == 1:
                dic_class_t.pop(key_t)
                dic_score_t.pop(len(key_t))
            else:
                dic_class_t.pop(key_t)
                dic_score_t[len(key_t)] -=1
        return (dic_class_t.copy(), dic_score_t.copy())

    # use get the data for visualization
    def visualization(self,path_t,name):#
        if len(self.score_keeper_new) == 0 and len(self.score_keeper_pro)==0:  # cheek the if the patterncheer function is run
            print("You have to run patterncheeker function first")
            return 0
        dicjsonsaver={} # use to save the data for saving the json
        path_f = ""
        score_t =""
        wrong_dic = {}
        right_dic = {}
        change_dic = {}
        now_action_dic =[]

        self.shortptdeleter()
        score_t = str(self.scorecalculater_ave())
        wrong_dic = self.dicFramegeter(self.dic_action_wrong)
        right_dic = self.dicFramegeter(self.dic_action_right)
        change_dic = self.dicFramegeter(self.dic_action_change)
        # only the action dic have the name of action , the rest of the dic only have the symbol of the actin
        now_action_dic = self.dicFramegeter4list(self.actiongeter_t(self.ac_list_com)) #需要对list格式做一个复原frame的
        now_action_dic_char = self.dicFramegeter4list(self.ac_list_com)
        print(now_action_dic)
        # write the data
        dicjsonsaver["score"]=score_t
        dicjsonsaver["wrongdic"] = wrong_dic
        dicjsonsaver["rightdic"] = right_dic
        dicjsonsaver["changedic"] = change_dic
        dicjsonsaver["nowaction"] = now_action_dic
        dicjsonsaver["nowaction_c"] = now_action_dic_char

        path_f = path_t+str(name)+".json"
        with open(path_f,"w+") as f:
            json.dump(dicjsonsaver,f)


if __name__ == '__main__':
    CHOOSE = 0
    # path_tttt2 = "/Users/syao/desktop/res/TeaSys_Dev_new_action48_10/"
    path_tttt2 = "/Users/syao/desktop/res/TeaSys_Dev_new_action48_10_ver3/"
    if not os.path.exists(path_tttt2):
        os.makedirs(path_tttt2)
    # # 为了提高速度 可以 之前就通过老手和新手库的程序获取老手和新手的数据并对比
    # # prot = ProTeacher("Tom", "/Users/syao/desktop/res/test_ori_1.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    # # prot.pfdicSaver()
    # # newt = NewTeacher("Mike", "/Users/syao/desktop/res/test_ori_2.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    # # newt.pfdicSaver()
    # # t = TestTeacher("Jimy", "/Users/syao/desktop/res/test_ori_4.csv")
    # # 如何处理同名的情况

    #contest_1 5
    # newt_1 = NewTeacher("AkiOkubo", "/Users/syao/desktop/res/csvdata/01_Rookie_AkiOkubo_English_all.csv", path_tttt2)#1
    # newt_1.pfdicSaver()#これが新人のデータcsv、名前、PATH、savepath,下のこの関数は保存する関数
    #
    # newt_2 = NewTeacher("KotaroHosoi", "/Users/syao/desktop/res/csvdata/02_Rookie_KotaroHosoi_Mathematics_all.csv", path_tttt2)#2
    # newt_2.pfdicSaver()
    #
    # newt_3 = NewTeacher("ShioriMasuko", "/Users/syao/desktop/res/csvdata/03_Rookie_ShioriMasuko_English_all.csv", path_tttt2)#3
    # newt_3.pfdicSaver()
    #
    # newt_4 = NewTeacher("YukinaHachisu", "/Users/syao/desktop/res/csvdata/04_Rookie_YukinaHachisu_English_all.csv", path_tttt2)#4
    # newt_4.pfdicSaver()
    #
    # newt_5 = NewTeacher("YusukeHachisu", "/Users/syao/desktop/res/csvdata/05_Rookie_YusukeHachisu_Japanese_all.csv", path_tttt2)#5
    # newt_5.pfdicSaver()
    #
    # #kojima and nishiyama 7
    # newt_6 = NewTeacher("Kojima1", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_01_all.csv", path_tttt2)#6
    # newt_6.pfdicSaver()
    # newt_7 = NewTeacher("Kojima2", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_02_all.csv", path_tttt2)#7
    # newt_7.pfdicSaver()
    # newt_8 = NewTeacher("Kojima3", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_03_all.csv", path_tttt2)#8
    # newt_8.pfdicSaver()
    # newt_9 = NewTeacher("Kojima4", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_04_all.csv",
    #                     path_tttt2)
    # newt_9.pfdicSaver()
    # newt_10 = NewTeacher("Kojima5", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_05_all.csv",
    #                     path_tttt2)
    # newt_10.pfdicSaver()
    # newt_11 = NewTeacher("Kojima6", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_06_all.csv",
    #                     path_tttt2)
    # newt_11.pfdicSaver()
    # newt_12 = NewTeacher("Kojima7", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_07_all.csv",
    #                     path_tttt2)
    # newt_12.pfdicSaver()
    #
    # #contest_2 6
    # newt_13 = NewTeacher("KiyoshiMori", "/Users/syao/desktop/res/csv_teaching_cont_2/01_Pf_KiyoshiMori_Mathematics_all.csv",
    #                     path_tttt2)
    # newt_13.pfdicSaver()
    # newt_14 = NewTeacher("RyotaTakahashi",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/03_Pre_RyotaTakahashi_Mathematics_all.csv",
    #                      path_tttt2)
    # newt_14.pfdicSaver()
    # newt_15 = NewTeacher("KenjiShiraishi",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/05_Pre_KenjiShiraishi_Mathematics_all.csv",
    #                      path_tttt2)
    # newt_15.pfdicSaver()
    # newt_16 = NewTeacher("HiroyukiKama",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/06_Pre_HiroyukiKama_Mathematics_all.csv",
    #                      path_tttt2)
    # newt_16.pfdicSaver()
    # newt_17 = NewTeacher("SatoshiNomuri",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/07_Pf_SatoshiNomuri_Mathematics_all.csv",
    #                      path_tttt2)
    # newt_17.pfdicSaver()
    # newt_18 = NewTeacher("ShioriMashiko",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/23_Pf_ShioriMashiko_English_all.csv",
    #                      path_tttt2)
    # newt_18.pfdicSaver()
    #
    # information class
    # newt_19 = NewTeacher("taiji",
    #                      "/Users/syao/desktop/res/information_class_edited/002_taiji_all.csv",
    #                      path_tttt2)
    # newt_19.pfdicSaver()
    # newt_20 = NewTeacher("kawazaki",
    #                      "/Users/syao/desktop/res/information_class_edited/004_kawazaki_all.csv",
    #                      path_tttt2)
    # newt_20.pfdicSaver()
    # newt_21 = NewTeacher("yabuuchi",
    #                      "/Users/syao/desktop/res/information_class_edited/005_yabuuchi_all.csv",
    #                      path_tttt2)
    # newt_21.pfdicSaver()
    # newt_22 = NewTeacher("nakanishi",
    #                      "/Users/syao/desktop/res/information_class_edited/006_nakanishi_all.csv",
    #                      path_tttt2)
    # newt_22.pfdicSaver()
    # newt_23 = NewTeacher("tsuda",
    #                      "/Users/syao/desktop/res/information_class_edited/007_tsuda_all.csv",
    #                      path_tttt2)
    # newt_23.pfdicSaver()
    # newt_24 = NewTeacher("shotani",
    #                      "/Users/syao/desktop/res/information_class_edited/008_shotani_all.csv",
    #                      path_tttt2)
    # newt_24.pfdicSaver()
    # newt_25 = NewTeacher("iwamoto",
    #                      "/Users/syao/desktop/res/information_class_edited/009_iwamoto_all.csv",
    #                      path_tttt2)
    # newt_25.pfdicSaver()# 新任データ２５個
    #
    # #contest_1 8　#同じく熟練データ
    # prot_1 = ProTeacher("YoshimitauHamada", "/Users/syao/desktop/res/csvdata/06_Expert_YoshimitauHamada_Mathematics_all.csv", path_tttt2)
    # prot_1.pfdicSaver()
    # prot_2 = ProTeacher("ShotaYoshida", "/Users/syao/desktop/res/csvdata/07_Expert_ShotaYoshida_Mathematics_NOFULL_all.csv", path_tttt2)
    # prot_2.pfdicSaver()
    # prot_3 = ProTeacher("TakashiMajima", "/Users/syao/desktop/res/csvdata/08_Expert_TakashiMajima_Mathematics_NOFULL_all.csv", path_tttt2)
    # prot_3.pfdicSaver()
    # prot_4 = ProTeacher("KunihiroSato", "/Users/syao/desktop/res/csvdata/09_Expert_KunihiroSato_Mathematics_all.csv", path_tttt2)
    # prot_4.pfdicSaver()
    # prot_5 = ProTeacher("AyakoYamamoto", "/Users/syao/desktop/res/csvdata/10_Expert_AyakoYamamoto_Japanese_all.csv", path_tttt2)
    # prot_5.pfdicSaver()
    # prot_6 = ProTeacher("SakiWatanabe", "/Users/syao/desktop/res/csvdata/11_Expert_SakiWatanabe_English_Champion_all.csv", path_tttt2)
    # prot_6.pfdicSaver()
    # prot_7 = ProTeacher("RinaAndo", "/Users/syao/desktop/res/csvdata/12_Expert_RinaAndo_Civics_all.csv", path_tttt2)
    # prot_7.pfdicSaver()
    # prot_8 = ProTeacher("NaokiSaiba", "/Users/syao/desktop/res/csvdata/13_Expert_NaokiSaiba_Science_all.csv", path_tttt2)
    # prot_8.pfdicSaver()
    #
    #
    # #contest_2 8
    # prot_9 = ProTeacher("MasahiroWatanabe2",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/08_Pf_MasahiroWatanabe_Mathematics_all.csv",
    #                      path_tttt2)
    # prot_9.pfdicSaver()
    # prot_10 = ProTeacher("MasahiroWatanabe1",
    #                     "/Users/syao/desktop/res/csv_teaching_cont_2/04_Pre_MasahiroWatanabe_Mathematics_all.csv",
    #                     path_tttt2)
    # prot_10.pfdicSaver()
    # prot_11 = ProTeacher("MasahiroWatanabe3",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/18_Fin_MasahiroWatanabe_Mathematics_all.csv",
    #                      path_tttt2)
    # prot_11.pfdicSaver()
    # prot_12 = ProTeacher("YusukeKimura",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/09_Fin_YusukeKimura_Science_all.csv",
    #                      path_tttt2)
    # prot_12.pfdicSaver()
    # prot_13 = ProTeacher("IppeiTakahira1",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/17_Pf_IppeiTakahira_English_all.csv",
    #                      path_tttt2)
    # prot_13.pfdicSaver()
    # prot_14 = ProTeacher("IppeiTakahira2",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/20_Fin_IppeiTakahira_English_all.csv",
    #                      path_tttt2)
    # prot_14.pfdicSaver()
    # prot_15 = ProTeacher("IkuTadame",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/19_Fin_IkuTadame_Japanese_all.csv",
    #                      path_tttt2)
    # prot_15.pfdicSaver()
    # prot_16 = ProTeacher("SatoshiIkeuchi",
    #                      "/Users/syao/desktop/res/csv_teaching_cont_2/21_Fin_SatoshiIkeuchi_Society_all.csv",
    #                      path_tttt2)
    # prot_16.pfdicSaver()
    #
    # #kojima and nishiyama 3
    # prot_17 = ProTeacher("Nishiyama1", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_01_all.csv",
    #                     path_tttt2)
    # prot_17.pfdicSaver()
    # prot_18 = ProTeacher("Nishiyama2", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_02_all.csv",
    #                     path_tttt2)
    # prot_18.pfdicSaver()
    # prot_19 = ProTeacher("Nishiyama3", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_03_all.csv",
    #                     path_tttt2)
    # prot_19.pfdicSaver()#熟練データ19個、
    #　#この前の部分は前处理で、新なデータを分析する時だけに使う必要がある
    #分析したデータは全部path_tttt2に保存した
    # ----------------------------------------------------前处理分界线-------------------------------------------------------

    if (CHOOSE==0):
        # 这个以后的数据一定会变成100 或者是0 表明还是记住了用户的特征的
        # 在ny和kj当中 他们的分数变化也正明了是会学习的，那么重要的地方就是数据量了
        # t = TestTeacher("AyakoYamamoto", "/Users/syao/desktop/res/csvdata/10_Expert_AyakoYamamoto_Japanese_all.csv")
        # t = TestTeacher("KunihiroSato", "/Users/syao/desktop/res/csvdata/09_Expert_KunihiroSato_Mathematics_all.csv")
        # t = TestTeacher("NaokiSaiba", "/Users/syao/desktop/res/csvdata/13_Expert_NaokiSaiba_Science_all.csv")
        # t = TestTeacher("RinaAndo", "/Users/syao/desktop/res/csvdata/12_Expert_RinaAndo_Civics_all.csv")
        # t = TestTeacher("SakiWatanabe", "/Users/syao/desktop/res/csvdata/11_Expert_SakiWatanabe_English_Champion_all.csv")
        # t = TestTeacher("Kojima", "/Users/syao/desktop/res/kj_v2.csv")
        # t = TestTeacher("Nishiyama", "/Users/syao/desktop/res/ny_v2.csv")



        # t = TestTeacher("AkiOkubo", "/Users/syao/desktop/res/csvdata/01_Rookie_AkiOkubo_English_all.csv") #1
        # t = TestTeacher("KotaroHosoi", "/Users/syao/desktop/res/csvdata/02_Rookie_KotaroHosoi_Mathematics_all.csv") #2
        # t = TestTeacher("ShioriMasuko", "/Users/syao/desktop/res/csvdata/03_Rookie_ShioriMasuko_English_all.csv") #3
        # t = TestTeacher("YukinaHachisu", "/Users/syao/desktop/res/csvdata/04_Rookie_YukinaHachisu_English_all.csv") #4
        # t = TestTeacher("YusukeHachisu", "/Users/syao/desktop/res/csvdata/05_Rookie_YusukeHachisu_Japanese_all.csv") #5
        # t = TestTeacher("Kojima1", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_01_all.csv") #6
        # t = TestTeacher("Kojima2", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_02_all.csv") #7
        # t = TestTeacher("Kojima3", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_03_all.csv") #8
        # t = TestTeacher("Kojima4", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_04_all.csv") #9
        # t = TestTeacher("Kojima5", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_05_all.csv") #10
        # t = TestTeacher("Kojima6", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_06_all.csv") #11
        # t = TestTeacher("Kojima7", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_07_all.csv") #12
        # t = TestTeacher("KiyoshiMori", "/Users/syao/desktop/res/csv_teaching_cont_2/01_Pf_KiyoshiMori_Mathematics_all.csv") #13
        # t = TestTeacher("RyotaTakahashi", "/Users/syao/desktop/res/csv_teaching_cont_2/03_Pre_RyotaTakahashi_Mathematics_all.csv") #14
        # t = TestTeacher("KenjiShiraishi", "/Users/syao/desktop/res/csv_teaching_cont_2/05_Pre_KenjiShiraishi_Mathematics_all.csv") #15
        # t = TestTeacher("HiroyukiKama", "/Users/syao/desktop/res/csv_teaching_cont_2/06_Pre_HiroyukiKama_Mathematics_all.csv") #16
        # t = TestTeacher("SatoshiNomuri", "/Users/syao/desktop/res/csv_teaching_cont_2/07_Pf_SatoshiNomuri_Mathematics_all.csv") #17
        # t = TestTeacher("ShioriMashiko", "/Users/syao/desktop/res/csv_teaching_cont_2/23_Pf_ShioriMashiko_English_all.csv") #18

        # t = TestTeacher("YoshimitauHamada", "/Users/syao/desktop/res/csvdata/06_Expert_YoshimitauHamada_Mathematics_all.csv") #19
        # t = TestTeacher("ShotaYoshida", "/Users/syao/desktop/res/csvdata/07_Expert_ShotaYoshida_Mathematics_NOFULL_all.csv") #20
        # t = TestTeacher("TakashiMajima", "/Users/syao/desktop/res/csvdata/08_Expert_TakashiMajima_Mathematics_NOFULL_all.csv") #21
        # t = TestTeacher("KunihiroSato", "/Users/syao/desktop/res/csvdata/09_Expert_KunihiroSato_Mathematics_all.csv") #22
        # t = TestTeacher("AyakoYamamoto", "/Users/syao/desktop/res/csvdata/10_Expert_AyakoYamamoto_Japanese_all.csv") #23
        # t = TestTeacher("SakiWatanabe", "/Users/syao/desktop/res/csvdata/11_Expert_SakiWatanabe_English_Champion_all.csv") #24
        # t = TestTeacher("RinaAndo", "/Users/syao/desktop/res/csvdata/12_Expert_RinaAndo_Civics_all.csv") #25
        # t = TestTeacher("NaokiSaiba", "/Users/syao/desktop/res/csvdata/13_Expert_NaokiSaiba_Science_all.csv") #26
        # t = TestTeacher("Nishiyama1", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_01_all.csv") #27
        # t = TestTeacher("Nishiyama2", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_02_all.csv") #28
        # t = TestTeacher("MasahiroWatanabe2", "/Users/syao/desktop/res/csv_teaching_cont_2/08_Pf_MasahiroWatanabe_Mathematics_all.csv") #29
        # t = TestTeacher("MasahiroWatanabe1", "/Users/syao/desktop/res/csv_teaching_cont_2/04_Pre_MasahiroWatanabe_Mathematics_all.csv") #30
        # t = TestTeacher("MasahiroWatanabe3", "/Users/syao/desktop/res/csv_teaching_cont_2/18_Fin_MasahiroWatanabe_Mathematics_all.csv") #31
        # t = TestTeacher("YusukeKimura", "/Users/syao/desktop/res/csv_teaching_cont_2/09_Fin_YusukeKimura_Science_all.csv") #32
        # t = TestTeacher("IppeiTakahira1", "/Users/syao/desktop/res/csv_teaching_cont_2/17_Pf_IppeiTakahira_English_all.csv") #33
        # t = TestTeacher("IppeiTakahira2", "/Users/syao/desktop/res/csv_teaching_cont_2/20_Fin_IppeiTakahira_English_all.csv") #34
        # t = TestTeacher("IkuTadame", "/Users/syao/desktop/res/csv_teaching_cont_2/19_Fin_IkuTadame_Japanese_all.csv") #35
        # t = TestTeacher("SatoshiIkeuchi", "/Users/syao/desktop/res/csv_teaching_cont_2/21_Fin_SatoshiIkeuchi_Society_all.csv") #36
        t = TestTeacher("Nishiyama3", "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_03_all.csv") #37
        #これがテストする、検証する教員のデータ
        # t = TestTeacher("tester", "/Users/syao/desktop/res/testdata.csv") # test only



        # path_tttt="/Users/syao/desktop/res/TeaSys_Dev_new_action48_10_ver2/" # 用了kojima方法的数据
        path_tttt="/Users/syao/desktop/res/TeaSys_Dev_new_action48_10_ver3/" # 先のpath

        # # path_tttt="/Users/syao/desktop/res/TeaSys_Dev_new_action48_10/" #  没用kojima的数据

        # # # new
        t.jsonReader_pf_onetime(path_tttt,"AkiOkubo",0)#このpathからデータを読む　path、名前（ファイル名）、０は新任１は熟練
        t.jsonReader_pf_onetime(path_tttt,"KotaroHosoi",0)#需要命名来识别
        t.jsonReader_pf_onetime(path_tttt,"ShioriMasuko",0)
        t.jsonReader_pf_onetime(path_tttt,"YukinaHachisu",0)
        t.jsonReader_pf_onetime(path_tttt,"YusukeHachisu",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima1",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima2",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima3",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima4",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima5",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima6",0)
        t.jsonReader_pf_onetime(path_tttt,"Kojima7",0)
        t.jsonReader_pf_onetime(path_tttt,"KiyoshiMori",0)
        t.jsonReader_pf_onetime(path_tttt,"RyotaTakahashi",0)
        t.jsonReader_pf_onetime(path_tttt,"KenjiShiraishi",0)
        t.jsonReader_pf_onetime(path_tttt,"HiroyukiKama",0)
        t.jsonReader_pf_onetime(path_tttt,"SatoshiNomuri",0)
        t.jsonReader_pf_onetime(path_tttt,"ShioriMashiko",0)
        t.jsonReader_pf_onetime(path_tttt,"taiji",0)
        t.jsonReader_pf_onetime(path_tttt,"kawazaki",0)
        t.jsonReader_pf_onetime(path_tttt,"yabuuchi",0)
        t.jsonReader_pf_onetime(path_tttt,"nakanishi",0)
        t.jsonReader_pf_onetime(path_tttt,"tsuda",0)
        t.jsonReader_pf_onetime(path_tttt,"shotani",0)
        t.jsonReader_pf_onetime(path_tttt,"iwamoto",0)


        # #
        # #
        # # # pro
        t.jsonReader_pf_onetime(path_tttt, "YoshimitauHamada", 1) # 1 = pro
        t.jsonReader_pf_onetime(path_tttt, "ShotaYoshida", 1)
        t.jsonReader_pf_onetime(path_tttt, "TakashiMajima", 1)
        t.jsonReader_pf_onetime(path_tttt, "KunihiroSato", 1)
        t.jsonReader_pf_onetime(path_tttt, "AyakoYamamoto", 1)
        t.jsonReader_pf_onetime(path_tttt, "SakiWatanabe", 1)
        t.jsonReader_pf_onetime(path_tttt, "RinaAndo", 1)
        t.jsonReader_pf_onetime(path_tttt, "NaokiSaiba", 1)
        t.jsonReader_pf_onetime(path_tttt, "Nishiyama1", 1)
        t.jsonReader_pf_onetime(path_tttt, "Nishiyama2", 1)
        # t.jsonReader_pf_onetime(path_tttt, "Nishiyama3", 1)　#これがテストに使いましたので、
        t.jsonReader_pf_onetime(path_tttt, "MasahiroWatanabe2", 1)
        t.jsonReader_pf_onetime(path_tttt, "MasahiroWatanabe1", 1)
        t.jsonReader_pf_onetime(path_tttt, "MasahiroWatanabe3", 1)
        t.jsonReader_pf_onetime(path_tttt, "YusukeKimura", 1)
        t.jsonReader_pf_onetime(path_tttt, "IppeiTakahira1", 1)
        t.jsonReader_pf_onetime(path_tttt, "IppeiTakahira2", 1)
        t.jsonReader_pf_onetime(path_tttt, "IkuTadame", 1)
        t.jsonReader_pf_onetime(path_tttt, "SatoshiIkeuchi", 1)


        # print("new size")
        # print(len(t.pf_temp_saver_new_2))
        # print(t.pf_temp_saver_new_2)
        # print(len(t.pf_temp_saver_new_3))
        # print(t.pf_temp_saver_new_3)
        # print(len(t.pf_temp_saver_new_4))
        # print(t.pf_temp_saver_new_4)
        # print(len(t.pf_temp_saver_new_5))
        # print(t.pf_temp_saver_new_5)
        # print(len(t.pf_temp_saver_new_6))
        # print(t.pf_temp_saver_new_6)
        # print(len(t.pf_temp_saver_new_7))
        # print(t.pf_temp_saver_new_7)
        # print(len(t.pf_temp_saver_new_8))
        # print(t.pf_temp_saver_new_8)
        # print(len(t.pf_temp_saver_new_9))
        # print(t.pf_temp_saver_new_9)
        # print(len(t.pf_temp_saver_new_10))
        # print(t.pf_temp_saver_new_10)
        # print("pro size")
        # print(len(t.pf_temp_saver_pro_2))
        # print(t.pf_temp_saver_pro_2)
        # print(len(t.pf_temp_saver_pro_3))
        # print(t.pf_temp_saver_pro_3)
        # print(len(t.pf_temp_saver_pro_4))
        # print(t.pf_temp_saver_pro_4)
        # print(len(t.pf_temp_saver_pro_5))
        # print(t.pf_temp_saver_pro_5)
        # print(len(t.pf_temp_saver_pro_6))
        # print(t.pf_temp_saver_pro_6)
        # print("**********************")
        #　cheek the times of the pattern in the dataset
        print("pro time")
        print(main.tools.order_dic((main.tools.timecounter(t.dicMergerforPro(1))))) #これがデータセットにtopのパータンです
        print("New time")
        print(main.tools.order_dic((main.tools.timecounter(t.dicMergerforNew(1)))))
        #
        # print(t.dicCommenShowerOnetime_v2() ) # 展示共通的set
        # print(t.dicCommenShowerOnetime_v3() ) # 展示共通的set 这个是递归删除包含的部分，时间比较久不建议用

        #
        t.dicCommonDeleteOnetime()  # 删除共通的部分、共通な部分を消す
        print("pro time")
        print(main.tools.order_dic_val(t.dicMergerforPro(1)))  # 这个是没删除共通的部分
        print("New time")
        print(main.tools.order_dic_val(t.dicMergerforNew(1)))
        #
        # # here to use the actionrewriter to rewriter the action list
        # # test teacher 不用抽出pattern 但是还是需要压缩动作
        #这个被压缩的数据用来当做当前的动作，
        t.compressList_id_t(main.tools.actionrewriter(t.ac_list_ori), 4, 8) # 这一步是压缩 原始数据，但是为什么写在外面 # TODO（Zake Yao）:把他写到程序里面去封装起来
        #これが動作抽出の操作、論文にある、4~8->1動作
        print("summ")
        # print(len(main.tools.actionrewriter(t.ac_list_ori)))
        print(len(t.ac_list_ori))
        # t.compressList_id_t(t.ac_list_ori, 4, 8) # 这一步是压缩 原始数据，但是为什么写在外面 # TODO（Zake Yao）:把他写到程序里面去封装起来
        summmm=0
        for x in t.dic_com_ori:
            summmm += t.dic_com_ori[x]
        print(summmm)
        # # # print(len(t.ac_list_ori))  # 1001
        #patternCheeker的参数数字表示是从2到几的进行统计
        maxlen = 8 # use this to change the maxlen
        #これがパターン長さの最大値、いまは８
        t.patternCheeker(maxlen)  # 这个是主要步骤的用sliping window 来cheek，和直接用pf解析不同的是，只能获取统计已有的pattern出现了多少
        # これがpattern 抽出、論文にある


        # print("new size")
        # print(len(t.pf_temp_saver_new_2))
        # print(len(t.pf_temp_saver_new_3))
        # print(len(t.pf_temp_saver_new_4))
        # print(len(t.pf_temp_saver_new_5))
        # print(len(t.pf_temp_saver_new_6))
        # print("pro size")
        # print(len(t.pf_temp_saver_pro_2))
        # print(len(t.pf_temp_saver_pro_3))
        # print(len(t.pf_temp_saver_pro_4))
        # print(len(t.pf_temp_saver_pro_5))
        # print(len(t.pf_temp_saver_pro_6))
        # print("Ori:")
        # print("pro:")
        # print(t.class_keeper_pro)
        # print(t.score_keeper_pro)
        # print("New:")
        # print(t.class_keeper_new)
        # print(t.score_keeper_new)

        t.patterncleanerfortesttea(1)  # use to delete the pattern which only show one time ，这个是用来删除只出现1次的情况，而且class和score都会更新
        #これが出現回数が１のパターンを消す
        # print("After delete the one time action:")
        # print("pro:")
        # print(t.class_keeper_pro)
        # print(t.score_keeper_pro)
        # print("New:")
        # print(t.class_keeper_new)
        # print(t.score_keeper_new)
        # 查错系列
        print("wrong:")
        print(t.dic_action_wrong)   # 动作数：错的是啥
        t.dicPatternReviser(maxlen) # これが修正機能
        print("right:")
        print(t.dic_action_right)
        print("change")
        print(t.dic_action_change)  # 没有对应的修改就是一个空的字符串
        print("Done!")
        print(t.dic_com_ori)
        print(len(t.ac_list_com))
        print("right:")
        print(main.tools.order_dic(t.dicFramegeter(t.dic_action_right)))
        print("Wrong")
        print(main.tools.order_dic(t.dicFramegeter(t.dic_action_wrong))) # 这个是用来输出修正的
        print("change")
        print(main.tools.order_dic(t.dicFramegeter(t.dic_action_change))) # 这个是用来输出修正的

        print("sum")
        print(main.tools.sumup(t.dic_com_ori))
        t.visualization("/Users/syao/desktop/res/visualizationdata/",t.name) #生成可视化的json文件
        #これが可視化のjsonを生成、可視化のvideoに使います
        # 算分系列
        # print("Score:") # tfidf和cheeker无关
        # print(main.tools.TF_IDF_Compute(t.teacherlist("/Users/syao/desktop/res/TeaSys_Dev/all_pattern/"), t.testpfFinder(1)))
        # print()
        # print(t.scorecalculater_jd(1))
        # print("score:ave:")
        # print(t.scorecalculater_ave())
        # print("longer:")
        # t.shortptdeleter()# 删除包括的部分，他直接删除了成员函数里面的数据
        # #
        # #
        print("score:ave:")
        print(t.scorecalculater_ave())#これがスコアを計算
        # # print("pro:")
        # print(t.class_keeper_pro)
        # print(t.score_keeper_pro)
        # print("New:")
        # print(t.class_keeper_new)
        # print(t.score_keeper_new)

        # to find out how long for the pattern is best
        # print("pro time")#删了共通的部分
        # print(main.tools.order_dic(main.tools.timecounter_v2(t.dicMergerforPro(1))))
        # print("New time")
        # print(main.tools.order_dic(main.tools.timecounter_v2(t.dicMergerforNew(1))))
        #
        # #删除包含的部分
        # print("pro time")
        # print(main.tools.order_dic(main.tools.timecounter_v2(main.tools.shortptdeleter_rel(t.dicMergerforPro(1)))))
        # print("New time")
        # print(main.tools.order_dic(main.tools.timecounter_v2(main.tools.shortptdeleter_rel(t.dicMergerforNew(1)))))
    elif(CHOOSE==1):#CHOOSEが１の時は、以上の過程を交差検証法でやりました、かくデータに対して、スコアを計算、csvの表を作る
        #----------------------------------------------自动写入分数的部分--------------------------------------------------
        teacher_dics = {"AkiOkubo": "/Users/syao/desktop/res/csvdata/01_Rookie_AkiOkubo_English_all.csv",  # new
                        "KotaroHosoi": "/Users/syao/desktop/res/csvdata/02_Rookie_KotaroHosoi_Mathematics_all.csv",
                        "ShioriMasuko": "/Users/syao/desktop/res/csvdata/03_Rookie_ShioriMasuko_English_all.csv",
                        "YukinaHachisu": "/Users/syao/desktop/res/csvdata/04_Rookie_YukinaHachisu_English_all.csv",
                        "YusukeHachisu": "/Users/syao/desktop/res/csvdata/05_Rookie_YusukeHachisu_Japanese_all.csv",
                        "Kojima1": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_01_all.csv",
                        "Kojima2": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_02_all.csv",
                        "Kojima3": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_03_all.csv",
                        "Kojima4": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_04_all.csv",
                        "Kojima5": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_05_all.csv",
                        "Kojima6": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_06_all.csv",
                        "Kojima7": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Kojima_07_all.csv",
                        "taiji": "/Users/syao/desktop/res/information_class_edited/002_taiji_all.csv",
                        "kawazaki": "/Users/syao/desktop/res/information_class_edited/004_kawazaki_all.csv",
                        "yabuuchi": "/Users/syao/desktop/res/information_class_edited/005_yabuuchi_all.csv",
                        "nakanishi": "/Users/syao/desktop/res/information_class_edited/006_nakanishi_all.csv",
                        "tsuda": "/Users/syao/desktop/res/information_class_edited/007_tsuda_all.csv",
                        "shotani": "/Users/syao/desktop/res/information_class_edited/008_shotani_all.csv",
                        "iwamoto": "/Users/syao/desktop/res/information_class_edited/009_iwamoto_all.csv",

                        # pro
                        "KiyoshiMori": "/Users/syao/desktop/res/csv_teaching_cont_2/01_Pf_KiyoshiMori_Mathematics_all.csv",
                        "RyotaTakahashi": "/Users/syao/desktop/res/csv_teaching_cont_2/03_Pre_RyotaTakahashi_Mathematics_all.csv",
                        "KenjiShiraishi": "/Users/syao/desktop/res/csv_teaching_cont_2/05_Pre_KenjiShiraishi_Mathematics_all.csv",
                        "HiroyukiKama": "/Users/syao/desktop/res/csv_teaching_cont_2/06_Pre_HiroyukiKama_Mathematics_all.csv",
                        "SatoshiNomuri": "/Users/syao/desktop/res/csv_teaching_cont_2/07_Pf_SatoshiNomuri_Mathematics_all.csv",
                        "ShioriMashiko": "/Users/syao/desktop/res/csv_teaching_cont_2/23_Pf_ShioriMashiko_English_all.csv",

                        "YoshimitauHamada": "/Users/syao/desktop/res/csvdata/06_Expert_YoshimitauHamada_Mathematics_all.csv",
                        "ShotaYoshida": "/Users/syao/desktop/res/csvdata/07_Expert_ShotaYoshida_Mathematics_NOFULL_all.csv",
                        "TakashiMajima": "/Users/syao/desktop/res/csvdata/08_Expert_TakashiMajima_Mathematics_NOFULL_all.csv",
                        "KunihiroSato": "/Users/syao/desktop/res/csvdata/09_Expert_KunihiroSato_Mathematics_all.csv",
                        "AyakoYamamoto": "/Users/syao/desktop/res/csvdata/10_Expert_AyakoYamamoto_Japanese_all.csv",
                        "RinaAndo":"/Users/syao/desktop/res/csvdata/12_Expert_RinaAndo_Civics_all.csv",
                        "NaokiSaiba":"/Users/syao/desktop/res/csvdata/13_Expert_NaokiSaiba_Science_all.csv",
                        "SakiWatanabe":"/Users/syao/desktop/res/csvdata/11_Expert_SakiWatanabe_English_Champion_all.csv",
                        "Nishiyama1": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_01_all.csv",
                        "Nishiyama2": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_02_all.csv",
                        "MasahiroWatanabe2": "/Users/syao/desktop/res/csv_teaching_cont_2/08_Pf_MasahiroWatanabe_Mathematics_all.csv",
                        "MasahiroWatanabe1": "/Users/syao/desktop/res/csv_teaching_cont_2/04_Pre_MasahiroWatanabe_Mathematics_all.csv",
                        "MasahiroWatanabe3": "/Users/syao/desktop/res/csv_teaching_cont_2/18_Fin_MasahiroWatanabe_Mathematics_all.csv",
                        "YusukeKimura": "/Users/syao/desktop/res/csv_teaching_cont_2/09_Fin_YusukeKimura_Science_all.csv",
                        "IppeiTakahira1": "/Users/syao/desktop/res/csv_teaching_cont_2/17_Pf_IppeiTakahira_English_all.csv",
                        "IppeiTakahira2": "/Users/syao/desktop/res/csv_teaching_cont_2/20_Fin_IppeiTakahira_English_all.csv",
                        "IkuTadame": "/Users/syao/desktop/res/csv_teaching_cont_2/19_Fin_IkuTadame_Japanese_all.csv",
                        "SatoshiIkeuchi": "/Users/syao/desktop/res/csv_teaching_cont_2/21_Fin_SatoshiIkeuchi_Society_all.csv",
                        "Nishiyama3": "/Users/syao/desktop/res/data_nishiyama_and_kojima_ver1/Nishiyama_03_all.csv",
                        }

        newteacher_list = ["KiyoshiMori","RyotaTakahashi", "KenjiShiraishi", "HiroyukiKama", "SatoshiNomuri", "ShioriMashiko",
            "AkiOkubo", "KotaroHosoi", "ShioriMasuko", "YukinaHachisu", "YusukeHachisu", "Kojima1",
                           "Kojima2", "Kojima3", "Kojima4", "Kojima5", "Kojima6", "Kojima7","taiji","kawazaki","yabuuchi","nakanishi","tsuda","shotani","iwamoto"]

        proteacher_list = [
                            "YoshimitauHamada", "ShotaYoshida", "TakashiMajima", "KunihiroSato", "AyakoYamamoto","RinaAndo",
                           "NaokiSaiba","SakiWatanabe","Nishiyama1", "Nishiyama2", "MasahiroWatanabe2", "MasahiroWatanabe1",
                           "MasahiroWatanabe3",
                           "YusukeKimura", "IppeiTakahira1", "IppeiTakahira2", "IkuTadame", "SatoshiIkeuchi", "Nishiyama3"]

        path_tttt = "/Users/syao/desktop/res/TeaSys_Dev_new_action48_10_ver3/"
        ccc=0
        numbb =8#最长的pt数、ここはパターン長さの最大値設置、今は８、毎回は１種類の長さ最大値を出力
        line_list =[]
        line_list.append("Name,Label,Score"+str(numbb)+",Score_del"+str(numbb)+",Correct score,Correct score_del\n")  # 添加表头
        for person in teacher_dics:
            ccc+=1
            newpro = "why" # 用于判断是否是新人，如果是新人就是new,老手就是pro基本不可能出现都不是的情况
            ifright = 2 # 用于判断是否正确，要是不正确就是2
            ifright_2 = 2 # 用于判断是否正确，要是不正确就是2
            t = TestTeacher(person, teacher_dics[person])# one test teacher
            for newteacher in newteacher_list:#只要不是当前作为test老师的data
                if newteacher != person:
                    t.jsonReader_pf_onetime(path_tttt, newteacher, 0)
            for proteacher in proteacher_list:
                if proteacher != person:
                    t.jsonReader_pf_onetime(path_tttt, proteacher, 1)
            # t.dicCommenShowerOnetime_v2()  #展示共通的部分
            t.dicCommonDeleteOnetime()  # 删除新人和老手共通的部分
            t.compressList_id_t(main.tools.actionrewriter(t.ac_list_ori), 4, 8)#压缩test老师的动作数据
            t.patternCheeker(numbb)  # 开始cheek ，这里的最长pattern为6，
            t.patterncleanerfortesttea(1)#删除匹配次数为1的pattern
            print("No"+str(ccc)+" "+person+"score:")#这里从零开始
            print("score:ave:")
            score_1 =t.scorecalculater_ave()
            print(score_1)
            print("longer:")
            t.shortptdeleter()  # 删除包括的部分，他直接删除了成员函数里面的数据
            print("score:ave:")
            score_2 =t.scorecalculater_ave()
            print(score_2)
            #用来判断他自己是老手还是新手
            if person in newteacher_list:
                newpro ="new"
                if score_1 >= 50:
                    ifright = 0
                elif score_1 < 50:
                    ifright = 1
                if score_2 >= 50:
                    ifright_2 = 0
                elif score_2 < 50:
                    ifright_2= 1
            elif person in proteacher_list:
                newpro = "pro"
                if score_1 >= 50:
                    ifright = 1
                elif score_1 < 50:
                    ifright = 0
                if score_2 >= 50:
                    ifright_2 = 1
                elif score_2 < 50:
                    ifright_2= 0

            linettt = person +","+newpro+","+str(score_1)+","+str(score_2)+","+str(ifright)+","+str(ifright_2)+"\n"
            line_list.append(linettt)

        with open("/Users/syao/desktop/res/score_result/result_"+str(numbb)+"_new.csv","w+") as fff:#写入到一个csv的里面
            fff.writelines(line_list)#ここに保存しました
        print(str(numbb)+"Done!!!")

