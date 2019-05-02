#!/usr/bin/env python
# encoding: utf-8
'''
@author: Zake Yao
@account: syao
@license: (C) Copyright 2015-2019, Media Experience Lab.
@contact: yaoshunyu96@gmail.com
@file: pattern_finder.py
@time: 2019-04-30 12:13
@desc:
'''

import os
import sys
import csv
# import pysnooper
import json


# arg[1]:times_span，this argument is the span of the repeat times
class PatternFinder(object):
    """docstring for PatternFinder"""

    def __init__(self, times_span, path):
        super(PatternFinder, self).__init__()
        # self.times_span = times_span
        self.csvpath = path  # "/Users/syao/desktop/res/kj.csv"
        self.dictemper = {}
        self.all_action_list = []  # read list
        self.com_action_list = []  # compressed list
        self.times_span = times_span # how many actions in one pattern

        #auto init
        self.all_action_list = self.csvReader_pf()
        self.com_action_list = self.compressList(self.all_action_list,2,4)
        self.dicMaker(self.com_action_list)



    #  read csv and use list to save it
    #  return must be a list
    def csvReader_pf(self):
        csv_file = csv.reader(open(self.csvpath))
        listoftemp = []
        for item in csv_file:
            # print type(item[0])
            listoftemp.append(item[0])
        return listoftemp

    #  use to compress the action list
    #  action times from a to b are seemed to be one action
    #  a is the least times and b is the most times
    def compressList(self, list_ac, a, b):
        counter_ac = 0
        temp_ac = ""
        temp_ac_list = []
        for x in list_ac:
            if (temp_ac == ""):  # to evaluate the initial value
                temp_ac = x
                counter_ac = 1
                continue
            if (temp_ac != x):  # see the next is different
                if (counter_ac < a):
                    temp_ac = x  #
                    continue
                if ((counter_ac <= b)):
                    temp_ac_list.append(temp_ac)  # add the last one
                if (counter_ac > b):
                    temp_conter_acs = counter_ac // b  # conclute how many times
                    for item in range(temp_conter_acs):
                        temp_ac_list.append(temp_ac)
                temp_ac = x
                counter_ac = 1

            else:
                counter_ac += 1
        if (counter_ac >= a):
            if (counter_ac <= b):
                temp_ac_list.append(temp_ac)
            else:
                temp_conter_acs = counter_ac // b  # conclute how many times
                for item in range(temp_conter_acs):
                    temp_ac_list.append(temp_ac)

        return temp_ac_list

    # use to change the action list into ID
    # return the ID of the action list for pattern
    def IDgeter(self, list_ac_k):
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

    # use to Decode the ID to the action list
    # return the action list
    def IDdecoder(self, str_id):
        list_t = []
        for char in str_id:
            f = open("/Users/syao/desktop/res/label_name.txt", "r")
            for temp_item in f.readlines():
                temp_item = temp_item.strip('\n')
                sp_temp_item = temp_item.split(",")
                if (str(char) == sp_temp_item[2]):
                    list_t.append(sp_temp_item[0])
            f.close()
        return list_t

    # use to make the pattern dic
    # use dic to save the pattern
    # @pysnooper.snoop()
    def dicMaker(self, list_ac):
        for x in range(len(list_ac)):
            temp_pat = []
            if ((x + self.times_span) <= len(list_ac)):
                for item in range(self.times_span):  # 3：0，1，2
                    temp_pat.append(list_ac[x + item])
                ID_temp = self.IDgeter(temp_pat)
                if (ID_temp in self.dictemper):
                    self.dictemper[ID_temp] = self.dictemper[ID_temp] + 1  # the time plus 1
                else:
                    self.dictemper[ID_temp] = 1  # make a new one

    # use to find if the pattern is in the dic and find out how many times
    # there is the pattern in the dic :ruturn the times
    # if not: return 0
    def dicFinder(self, str_ac):
        if (str_ac in self.dictemper):
            return self.dictemper[str_ac]
        else:
            print("ERROR!!!Do not have this pattern!!!")
            return 0

    # use to show the dic contents
    # return the whole dic of actions
    def dicShower(self):
        return self.dictemper

    # use to put the pattern in to she dic
    def dicPuter(self, str_ac):
        if (str_ac in self.dictemper):
            self.dictemper[str_ac] += 1  # if it was already in the dic,plus 1
        else:
            self.dictemper[str_ac] = 1  # if it was not in the dic,evalue it to 1
            print("Add a new pattern" + str_ac)

    # if the time in the dic for this action is less than k than delete this one
    def dicClear(self, k):
        dic_temp = self.dictemper.copy()
        for key in self.dictemper:
            if (dic_temp[key] <= k):
                dic_temp.pop(key)
        self.dictemper = dic_temp.copy()

    # use to save the pattern into json for future
    def dicSaver(self,save_path):
        json_str = json.dumps(self.dictemper)
        # with open("/Users/syao/desktop/res/pattern_save/pattern_data" + str(self.times_span) + ".json",
        with open(save_path + str(self.times_span) + ".json",
                  "w") as json_file:
            json_file.write(json_str)

    # use to save the whole pattern ID of video
    # return the list
    def AllPattern(self, list_ac):
        pass

    # use to came back to the NO. of frame
    # though the Pattern to the frame
    def dicBack():
        pass


if __name__ == '__main__':
    # 先建立对象
    # 再压缩
    # 再做字典
    pf = PatternFinder(3, "/Users/syao/desktop/res/kj.csv")  # build the object with the span of 4 times
    listofaction = []
    listofaction = pf.csvReader_pf()  # read the csv
    com_list = []
    com_list = pf.compressList(listofaction, 2, 4)  # 4rame~16frame,compress the csv list
    print(com_list)
    print(len(com_list))
    pf.dicMaker(com_list)  # to build the dic
    print(pf.dicFinder("AABD"))
    print(pf.dicShower())  # to show the sum of the dic
    pf.dicClear(1)  # clear the action when the time is less than 2(<=1)
    print(pf.dicShower())  # to show the sum of the new dic
    # ttt=['Point to the students', 'Standing and talking', 'Write on the blackboard']
    # print(pf.IDgeter(ttt))
    pf.dicSaver()  # save to the json
