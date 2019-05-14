#!/usr/bin/env python# encoding: utf-8'''@author: Zake Yao@account: syao@license: (C) Copyright 2015-2019, Media Experience Lab.@contact: yaoshunyu96@gmail.com@file: teacher.py@time: 2019-04-30 12:13@desc: This code is the main code include the object of the teacher,to build the objects of new teachers and professionalteachers to get the datebase , and than build the test teacher to use the datebase and get the score.'''import osimport csvimport sys# import pysnooperimport jsonimport stringfrom main.pattern_fineder import PatternFinderimport main.tools# the Teacher class to make instances include many pattern# arg[1]:csvpath is to the path of the csv which use to analyze# arg[2]:test_csvpath is to analyze and compare with the last oneclass Teacher(object):    """docstring for Teacher"""    def __init__(self, name,csvpath,save_path):  #        super(Teacher, self).__init__()        self.csvpath = csvpath        self.save_path = save_path        self.name = name        # for all the pattern        self.pf_2 = PatternFinder(2, csvpath)  # every pattern for teacher        self.pf_3 = PatternFinder(3, csvpath)        self.pf_4 = PatternFinder(4, csvpath)        self.pf_5 = PatternFinder(5, csvpath)        self.pf_6 = PatternFinder(6, csvpath)    def pfdicSaver(self):  # 他们两个是因为是要预先处理的所以得储存        # to build a new path when the path is wrong        full_path = self.save_path + "/" + str(self.name) + "/"        if not os.path.exists(full_path):  # if file is not existed            os.makedirs(full_path)        self.pf_2.dicSaver(full_path)  # save the data which span is 2        self.pf_3.dicSaver(full_path)  # save the data which span is 3        self.pf_4.dicSaver(full_path)  # save the data which span is 4        self.pf_5.dicSaver(full_path)  # save the data which span is 5        self.pf_6.dicSaver(full_path)  # save the data which span is 6    # use to save all the pattern in the list    # add the function to delete the one time pattern    def pfdicSaver_all(self,show_times):        dic_temp={}        full_path = self.save_path + "/all_pattern/" # 在一个all—pattern 里面存着所有的pt        if not os.path.exists(full_path):  # if file is not existed            os.makedirs(full_path)        dic_temp.update(self.pf_2.dicShower())        dic_temp.update(self.pf_3.dicShower())        dic_temp.update(self.pf_4.dicShower())        dic_temp.update(self.pf_5.dicShower())        dic_temp.update(self.pf_6.dicShower())        main.tools.patterncleaner(dic_temp,show_times) # use to delete the 1 time pattern        main.tools.dicSaver_rel(dic_temp, self.name, full_path)  # 通过name来区分每个json文件# This is the teacher with much experience# arg[2]:test_csvpath is to# arg[3]:name is the to identify each teacherclass ProTeacher(Teacher):    """docstring for Proteacher"""    def __init__(self, name, csvpath, save_path):        super(ProTeacher, self).__init__(name,csvpath,save_path)        self.csvpath = csvpath        self.save_path = save_path        self.name = name        # for all the pattern        self.pf_2 = PatternFinder(2, csvpath)  # every pattern for teacher        self.pf_3 = PatternFinder(3, csvpath)        self.pf_4 = PatternFinder(4, csvpath)        self.pf_5 = PatternFinder(5, csvpath)        self.pf_6 = PatternFinder(6, csvpath)# This is the teacher who is newclass NewTeacher(Teacher):    """docstring for NewTeacher"""    def __init__(self, name, csvpath, save_path):        super(NewTeacher, self).__init__(name,csvpath,save_path)        self.csvpath = csvpath        self.save_path = save_path        self.name = name        # for all the pattern        self.pf_2 = PatternFinder(2, csvpath)  # every pattern for teacher        self.pf_3 = PatternFinder(3, csvpath)        self.pf_4 = PatternFinder(4, csvpath)        self.pf_5 = PatternFinder(5, csvpath)        self.pf_6 = PatternFinder(6, csvpath)