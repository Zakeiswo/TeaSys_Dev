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
from main.teacher import Teacher
from main.teacher import NewTeacher
from main.teacher import ProTeacher


# This is the teacher who is going to be tested
class TestTeacher(object):
    """docstring for TestTeacher"""

    def __init__(self, name, test_csvpath):
        super(TestTeacher, self).__init__()
        self.name = name
        self.dic_com_ori = {}  # 压缩后下标：占了几个frame，注意补上被省略的,由于还原真正错的地方是哪一个帧数
        self.test_csvpath = test_csvpath
        # for proteacher data to calculate the score
        self.score_keeper_pro = {}
        self.class_keeper_pro = {}
        # for newteacher data to calculate the score
        self.score_keeper_new = {}
        self.class_keeper_new = {}
        self.ac_list_com = []  # 压缩后的list
        self.ac_list_ori = []  # 原始的list

        self.dic_action_wrong = {}  # 这里记录的只是 动作数：错的是啥，但是可以和dic_com_ori一起还原出哪里错了
        self.dic_action_wrong_fra = {}  # 记录帧数:错的是啥
        self.dic_action_right = {}
        self.dic_action_right_fra = {}

        # use to keep the json data
        # first is the pro patterns
        self.pf_temp_saver_pro_2 = {}
        self.pf_temp_saver_pro_3 = {}
        self.pf_temp_saver_pro_4 = {}
        self.pf_temp_saver_pro_5 = {}
        self.pf_temp_saver_pro_6 = {}
        # second is the new patterns
        self.pf_temp_saver_new_2 = {}
        self.pf_temp_saver_new_3 = {}
        self.pf_temp_saver_new_4 = {}
        self.pf_temp_saver_new_5 = {}
        self.pf_temp_saver_new_6 = {}

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
                self.pf_temp_saver_pro_6 = self.dicMerger(self.pf_temp_saver_pro_6.copy(), json_file.copy())

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
                self.pf_temp_saver_new_6 = self.dicMerger(self.pf_temp_saver_new_6.copy(), json_file.copy())

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

    # use to show the common pattern in the dic
    # return the same keys in a list
    def dicCommonShower(self, dict_1, dict_2):
        set_common = dict_1.keys() & dict_2.keys()  # set include the same keys in the dic
        return set_common

    def dicCommenShowerOnetime(self):
        print(self.dicCommonShower(self.pf_temp_saver_pro_2, self.pf_temp_saver_new_2))
        print(self.dicCommonShower(self.pf_temp_saver_pro_3, self.pf_temp_saver_new_3))
        print(self.dicCommonShower(self.pf_temp_saver_pro_4, self.pf_temp_saver_new_4))
        print(self.dicCommonShower(self.pf_temp_saver_pro_5, self.pf_temp_saver_new_5))
        print(self.dicCommonShower(self.pf_temp_saver_pro_6, self.pf_temp_saver_new_6))

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

    def patternCheeker(self):  # 只运行一次，再运行会刷新dict的
        # TODO(Zake Yao): add a function to find where is wrong
        # 统计每种出现了多少次
        pattern_temp = []
        temp_score_keeper_pro = {}
        temp_class_keeper_pro = {}
        temp_score_keeper_new = {}
        temp_class_keeper_new = {}
        for item in range(len(self.ac_list_com)):
            for x in range(6):
                if item + x < len(self.ac_list_com):
                    pattern_temp.append(self.ac_list_com[item + x])
                    if len(pattern_temp) == 2:  # 这里还需要更大的判断来判别是符合加分还是减分的字典了
                        pattern_str = (''.join(pattern_temp))
                        if pattern_str in self.pf_temp_saver_pro_2:
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
            pattern_temp.clear()  # clear the list for new pattern to cheek
        self.score_keeper_pro = temp_score_keeper_pro.copy()
        self.class_keeper_pro = temp_class_keeper_pro.copy()
        self.score_keeper_new = temp_score_keeper_new.copy()
        self.class_keeper_new = temp_class_keeper_new.copy()

    # use to forecast the next action witch one is best
    # input the pattern of now and return the best next action
    # if no next patern in the dic return ""
    def patternForecaster(self, pattern_temp):  # TODO(Zake Yao):需不需要添加一个flag用来判断有没有清楚共通的部分
        if len(pattern_temp) > 5:
            print("Error! The length of the pattern can't longer than 5.")
            sys.exit(1)
        if len(pattern_temp) < 1:
            print("Error! The length of the pattern can't shorter than 1.")
            sys.exit(1)
        if len(pattern_temp) == 1:  # cheek the length and return the frequency of the max one
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_2:
                if item[0] == pattern_temp:
                    if self.pf_temp_saver_pro_2[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_2[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 2:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_3:
                if item[0:2] == pattern_temp:
                    if self.pf_temp_saver_pro_3[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_3[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 3:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_4:
                if item[0:3] == pattern_temp:
                    if self.pf_temp_saver_pro_4[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_4[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 4:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_5:
                if item[0:4] == pattern_temp:
                    if self.pf_temp_saver_pro_5[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_5[item]
                        max_temp_item = item
            return max_temp_item
        elif len(pattern_temp) == 5:
            max_temp_num = 0
            max_temp_item = ""
            for item in self.pf_temp_saver_pro_6:
                if item[0:5] == pattern_temp:
                    if self.pf_temp_saver_pro_6[item] > max_temp_num:  # 但是这样只会变成一样的频度显示第一个
                        max_temp_num = self.pf_temp_saver_pro_6[item]
                        max_temp_item = item
            return max_temp_item

    # use to change the wrong pattern to the right pattern
    # by cheek the first some action of the pattern to use the function patternForecaster to get the right action
    def dicPatternReviser(self):  # 如果是这个动作老手里面没有对应的修改怎么办
        for item in self.dic_action_wrong:
            if len(self.dic_action_wrong[item][0:-1]) < 1:
                print("Error!It must be longer than 1 in the wrong action list")
                sys.exit(1)
            if len(self.dic_action_wrong[item][0:-1]) > 5:
                print("Error!It must be shorter than 5 in the wrong action list")
                sys.exit(1)
            # It will cheek the length auto automatically
            self.dic_action_right[item] = self.patternForecaster(str(self.dic_action_wrong[item])[0:-1])

    # use to get frame instead of action number in the dic
    # to rewrite the dic，return a new dic with frame
    def dicFramegeter(self, dic_temp):
        new_dic = {}
        for item in dic_temp:
            sum_temp = 0
            for x in self.dic_com_ori:
                # cheek
                if (item == x):
                    new_dic[sum_temp] = dic_temp[item]
                    break
                # then add
                sum_temp += self.dic_com_ori[x]
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
    def compressList_id_t(self, list_ac, a, b):  # 不看被省略的,应该是2~7
        counter_ac = 0
        counter_recover = 0
        temp_ac = ""
        temp_ac_list = []
        for x in list_ac:  # 没有加上最后一次
            if temp_ac == "":  # to evaluate the initial value
                temp_ac = x
                counter_ac = 1  # first time
                counter_recover = 0
                continue
            elif temp_ac != x:  # see the next is different
                if counter_ac < a:  # 结算当前的
                    counter_recover += (a - 1)  # 这个补上了1次的
                    temp_ac = x
                    if (counter_recover > 9):
                        print("Attention:Maybe error.It's hard for counter_recover to be over than 9!")
                    continue
                elif counter_ac <= b:
                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))  # add the last one
                    self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover
                elif counter_ac > b:  # 要是大于4的时候
                    temp_conter_acs = counter_ac // b  # conclute how many times
                    for item in range(temp_conter_acs):
                        temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                        self.dic_com_ori[len(temp_ac_list) - 1] = b
                    self.dic_com_ori[len(temp_ac_list) - 1] = b + counter_ac % b + (counter_recover)
                # 这个是每个下标和和原本对于的frame数
                # 基础的4个加上多于被省略，是4个是因为b是4
                # 包括取余省略的和小于2省略的
                temp_ac = x
                counter_ac = 1
                counter_recover = 0  # reflash
            else:
                counter_ac += 1
        if counter_ac >= a:  # use to add the last element# 最后一个元素如果是1的时候，给最后一个元素加一
            if counter_ac <= b:
                temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover
            else:
                temp_conter_acs = counter_ac // b  # conclute how many times
                for item in range(temp_conter_acs):
                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))
                    self.dic_com_ori[len(temp_ac_list) - 1] = b
                self.dic_com_ori[len(temp_ac_list) - 1] = b + counter_ac % b + (counter_recover)

        if (len(self.dic_com_ori) - len(self.ac_list_ori)) < a:  # when the last one is 1
            self.dic_com_ori[len(temp_ac_list) - 1] += a - 1

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


if __name__ == '__main__':
    # prot = ProTeacher("Tom", "/Users/syao/desktop/res/test_ori_1.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    # prot.pfdicSaver()
    # newt = NewTeacher("Mike", "/Users/syao/desktop/res/test_ori_2.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    # newt.pfdicSaver()
    # t = TestTeacher("Jimy", "/Users/syao/desktop/res/test_ori_4.csv")

    prot = ProTeacher("Tom", "/Users/syao/desktop/res/ny_v2.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    prot.pfdicSaver()
    newt = NewTeacher("Mike", "/Users/syao/desktop/res/kj_v2.csv", "/Users/syao/desktop/res/TeaSys_Dev")
    newt.pfdicSaver()
    prot.pfdicSaver_all(1)  # save the whole data
    newt.pfdicSaver_all(1)
    t = TestTeacher("Jimy", "/Users/syao/desktop/res/ny_test_4fornew.csv")

    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Tom/2.json", 2, 1)  # 1 for pro
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Tom/3.json", 3, 1)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Tom/4.json", 4, 1)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Tom/5.json", 5, 1)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Tom/6.json", 6, 1)

    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Mike/2.json", 2, 0)  # 0 for new
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Mike/3.json", 3, 0)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Mike/4.json", 4, 0)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Mike/5.json", 5, 0)
    t.jsonReader_pf("/Users/syao/desktop/res/TeaSys_Dev/Mike/6.json", 6, 0)

    print("new size")
    print(len(t.pf_temp_saver_new_2))
    print(t.pf_temp_saver_new_2)
    print(len(t.pf_temp_saver_new_3))
    print(t.pf_temp_saver_new_3)
    print(len(t.pf_temp_saver_new_4))
    print(t.pf_temp_saver_new_4)
    print(len(t.pf_temp_saver_new_5))
    print(t.pf_temp_saver_new_5)
    print(len(t.pf_temp_saver_new_6))
    print(t.pf_temp_saver_new_6)
    print("pro size")
    print(len(t.pf_temp_saver_pro_2))
    print(t.pf_temp_saver_pro_2)
    print(len(t.pf_temp_saver_pro_3))
    print(t.pf_temp_saver_pro_3)
    print(len(t.pf_temp_saver_pro_4))
    print(t.pf_temp_saver_pro_4)
    print(len(t.pf_temp_saver_pro_5))
    print(t.pf_temp_saver_pro_5)
    print(len(t.pf_temp_saver_pro_6))
    print(t.pf_temp_saver_pro_6)
    print("**********************")
    t.dicCommenShowerOnetime()  # 展示共通的set

    t.dicCommonDeleteOnetime()  # 删除共通的部分

    t.compressList_id_t(t.ac_list_ori, 2, 4)
    print(len(t.ac_list_ori))  # 1001

    t.patternCheeker()
    print("new size")
    print(len(t.pf_temp_saver_new_2))
    print(len(t.pf_temp_saver_new_3))
    print(len(t.pf_temp_saver_new_4))
    print(len(t.pf_temp_saver_new_5))
    print(len(t.pf_temp_saver_new_6))
    print("pro size")
    print(len(t.pf_temp_saver_pro_2))
    print(len(t.pf_temp_saver_pro_3))
    print(len(t.pf_temp_saver_pro_4))
    print(len(t.pf_temp_saver_pro_5))
    print(len(t.pf_temp_saver_pro_6))
    print("Ori:")
    print("pro:")
    print(t.class_keeper_pro)  # 为啥这个的4最大，也没有压缩啊
    print(t.score_keeper_pro)  # 为啥这个这么少
    print("New:")
    print(t.class_keeper_new)
    print(t.score_keeper_new)  # 为啥这么少
    # t.patterncleanerfortesttea(1)  # use to delete the pattern which only show one time
    print("After delete the one time action:")
    print("pro:")
    print(t.class_keeper_pro)
    print(t.score_keeper_pro)
    print("New:")
    print(t.class_keeper_new)
    print(t.score_keeper_new)
    print("wrong:")
    print(t.dic_action_wrong)
    t.dicPatternReviser()
    print("right:")
    print(t.dic_action_right)  # 没有对应的修改就是一个空的字符串
    print("Done!")
    print(t.dic_com_ori)
    print(len(t.ac_list_com))
    print(t.dicFramegeter(t.dic_action_wrong))
    print("Score:") # tfidf和cheeker无关
    print(main.tools.TF_IDF_Compute(t.teacherlist("/Users/syao/desktop/res/TeaSys_Dev/all_pattern/"),t.testpfFinder(1)))
    print()
    print(t.scorecalculater_jd(1))
