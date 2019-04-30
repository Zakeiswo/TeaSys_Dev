#!/usr/bin/env python# encoding: utf-8'''@author: Zake Yao@account: syao@license: (C) Copyright 2015-2019, Media Experience Lab.@contact: yaoshunyu96@gmail.com@file: teacher.py@time: 2019-04-30 12:13@desc:'''import osimport sysimport csv# import pysnooperimport jsonimport stringfrom main.pattern_fineder import PatternFinder# the Teacher class to make instances include many pattern# arg[1]:csvpath is to the path of the csv which use to analyze# arg[2]:test_csvpath is to analyze and compare with the last oneclass Teacher(object):    """docstring for Teacher"""    def __init__(self, csvpath,test_csvpath):#        super(Teacher, self).__init__()        self.csvpath = csvpath        self.test_csvpath =test_csvpath        #for all the pattern        self.pf_2 = PatternFinder(2, csvpath)  # every pattern for teacher        self.pf_3 = PatternFinder(3, csvpath)        self.pf_4 = PatternFinder(4, csvpath)        self.pf_5 = PatternFinder(5, csvpath)        self.pf_6 = PatternFinder(6, csvpath)        self.ac_list_ori = []        self.ac_list_com = []  # 这个需要吗        # to read the csv        csv_file = csv.reader(open(test_csvpath))        for item in csv_file:            self.ac_list_ori.append(item[0])    # read csv and use list to save it    # reflesh the list to the new csv    def csvReader_t(self):  # default path is in the object        csv_file = csv.reader(open(self.csvpath))        listoftemp = []        for item in csv_file:            # print type(item[0])            listoftemp.append(item[0])        if (len(listoftemp) == 0):            print("Error!Path maybe null")        self.ac_list_ori.clear()        self.ac_list_ori += listoftemp    # use to change the action list into ID    # return the ID of the action list for pattern    def IDgeter_t(self, list_ac_k):        temp_str = ""        for index in range(len(list_ac_k)):            temp_1 = list_ac_k[index]            f = open("/Users/syao/desktop/res/label_name.txt", "r")            for temp_item in f.readlines():                temp_item = temp_item.strip('\n')                sp_temp_item = temp_item.split(",")                if (temp_1 == sp_temp_item[0]):                    temp_str += sp_temp_item[2]                # print(sp_temp_item[2])            f.close()        return temp_str    # use to get the single ID for one action    def IDgeterforsingel_t(self, str_ac):        f = open("/Users/syao/desktop/res/label_name.txt", "r")        temp_str = ""        for temp_item in f.readlines():            temp_item = temp_item.strip('\n')            sp_temp_item = temp_item.split(",")            if (str_ac == sp_temp_item[0]):                temp_str = sp_temp_item[2]                break        f.close()        return temp_str# This is the teacher with much experience# arg[2]:test_csvpath is to# arg[3]:name is the to identify each teacherclass ProTeacher(Teacher):    """docstring for Proteacher"""    def __init__(self, csvpath,test_csvpath,name,save_path):        super(ProTeacher, self).__init__(csvpath,test_csvpath)        self.csvpath = csvpath        self.test_csvpath = test_csvpath        self.save_path = save_path    # TODO(Zake Yao): add a function to save the data for professional teacher    # use to save the data for the times of all patterns    def pfdicSaver(self):        # to build a new path        # TODO(Zake Yao):reflesh the paramater of name        name ="vvv"        if not os.path.exists(self.save_path+"/"+name+"/"):# if file is existed            os.makedirs(self.save_path+"/"+name+"/")        # 调用每个pf的save方法        pass# This is the teacher who is newclass NewTeacher(Teacher):    """docstring for NewTeacher"""    def __init__(self, csvpath,test_csvpath):        super(NewTeacher, self).__init__(csvpath,test_csvpath)        self.csvpath = csvpath        self.test_csvpath = test_csvpath    # TODO(Zake Yao): add a function to save the data for new teacher# This is the teacher who is going to be testedclass TestTeacher(Teacher):    """docstring for TestTeacher"""    def __init__(self, csvpath,test_csvpath):        super(TestTeacher, self).__init__(csvpath,test_csvpath)        self.dic_com_ori = {}  # 压缩后下标：占了几个frame，注意补上被省略的        self.csvpath = csvpath        self.test_csvpath = test_csvpath        self.score_keepr={}    # TODO(Zake Yao):Add a function to read the jsons that new teacher and old teacher's output    # use to find the pattern for this teacher    # to see when the tester do the wrong pattern    # to sum how many right pattern tester has down    def patternCheaker(self):        # TODO(Zake Yao): add a function to find where is wrong        pattern_temp=[]        temp_keeper={}        for item in range(len(self.ac_list_com)):            for x in range(6):                if(item+x<len(self.ac_list_com)):                    pattern_temp.append(self.ac_list_com[item+x])                    if(len(pattern_temp)==2):#这里还需要更大的判断来判别是符合加分还是减分的字典了                        if ((''.join(pattern_temp)) in self.pf_2.dictemper):                            if(2 in temp_keeper ):                                temp_keeper[2] += 1                            else:                                temp_keeper[2]=1                    elif(len(pattern_temp)==3):                        if ((''.join(pattern_temp)) in self.pf_3.dictemper):                            if (3 in temp_keeper):                                temp_keeper[3] += 1                            else:                                temp_keeper[3] = 1                    elif (len(pattern_temp) == 4):                        if ((''.join(pattern_temp)) in self.pf_4.dictemper):                            if (4 in temp_keeper):                                temp_keeper[4] += 1                            else:                                temp_keeper[4] = 1                    elif (len(pattern_temp) == 5):                        if ((''.join(pattern_temp)) in self.pf_5.dictemper):                            if (5 in temp_keeper):                                temp_keeper[5] += 1                            else:                                temp_keeper[5] = 1                    elif (len(pattern_temp) == 6):                        if ((''.join(pattern_temp)) in self.pf_6.dictemper):                            print(''.join(pattern_temp))                            if (6 in temp_keeper):                                temp_keeper[6] += 1                            else:                                temp_keeper[6] = 1            pattern_temp.clear()#clear the list for new pattern to cheak        self.score_keepr = temp_keeper.copy()        return self.score_keepr    # use to compress the list to the ID    # and build the dic to contact the 2 list    # return the list of the action list    # 不看被省略的应该是2~7    def compressList_id_t(self, list_ac, a, b):        counter_ac = 0        counter_recover = 0        temp_ac = ""        temp_ac_list = []        for x in list_ac:  # 没有加上最后一次            if (temp_ac == ""):  # to evaluate the initial value                temp_ac = x                counter_ac = 1  # first time                counter_recover = 0                continue            elif (temp_ac != x):  # see the next is different                if (counter_ac < a):  # 结算当前的                    counter_recover += (a - 1)  # 这个补上了1次的                    temp_ac = x                    if (counter_recover > 9):                        print("Attention:Maybe error.It's hard for counter_recover to be over than 9!")                    continue                elif ((counter_ac <= b)):                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))  # add the last one                    self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover                elif (counter_ac > b):  # 要是大于4的时候                    temp_conter_acs = counter_ac // b  # conclute how many times                    for item in range(temp_conter_acs):                        temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))                        self.dic_com_ori[len(temp_ac_list) - 1] = b                    self.dic_com_ori[len(temp_ac_list) - 1] = b + counter_ac % b + (counter_recover)                # 这个是每个下标和和原本对于的frame数                # 基础的4个加上多于被省略，是4个是因为b是4                # 包括取余省略的和小于2省略的                temp_ac = x                counter_ac = 1                counter_recover = 0  # reflash            else:                counter_ac += 1        if (counter_ac >= a):  # use to add the last element# 最后一个元素如果是1的时候，给最后一个元素加一            if (counter_ac <= b):                temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))                self.dic_com_ori[len(temp_ac_list) - 1] = counter_ac + counter_recover            else:                temp_conter_acs = counter_ac // b  # conclute how many times                for item in range(temp_conter_acs):                    temp_ac_list.append(self.IDgeterforsingel_t(temp_ac))                    self.dic_com_ori[len(temp_ac_list) - 1] = b                self.dic_com_ori[len(temp_ac_list) - 1] = b + counter_ac % b + (counter_recover)        if ((len(self.dic_com_ori) - len(self.ac_list_ori)) < a):  # when the last one is 1            self.dic_com_ori[len(temp_ac_list) - 1] += a - 1        self.ac_list_com.clear()        self.ac_list_com += temp_ac_list        return temp_ac_listif __name__ == '__main__':    t = TestTeacher("/Users/syao/desktop/res/kj_test_1.csv","/Users/syao/desktop/res/ny_test_1.csv")    t.compressList_id_t(t.ac_list_ori, 2, 4)    print(len(t.ac_list_ori))  # 8385    print(t.dic_com_ori)    sum = 0    for x in t.dic_com_ori:        sum += t.dic_com_ori[x]    print(sum)    #print(t.patternCheaker())#还是有240个    print(t.patternCheaker())