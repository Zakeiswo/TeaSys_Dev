#!/usr/bin/env python
# encoding: utf-8
'''
@author: Zake Yao
@account: syao
@license: (C) Copyright 2015-2019, Media Experience Lab.
@contact: yaoshunyu96@gmail.com
@file: tools
@time: 2019-05-09 15:00
@desc: to save the functions that don't use the class member parameter
'''
__author__ = 'Zake Yao'

import math
import json
import collections
from functools import reduce



# eg.{name1:{pt1:sum_num,pt2:sum_num,...}, name2:{...}...}
def TF_IDF_Compute(input_sets,words,if_weight = True): # 这个word是用来判断是不是关键字的

    word_in_afile_stat = {}
    word_in_allfiles_stat = {}
    # json_file = open(input_url, encoding='utf-8')
    # json_dic = json.load(json_file)
    # temp_file_name = input_url.split("/")[-1].split(".")[0] # leave only the name
    files_num = 0
    for item_x in input_sets:  # 这个data应该是一个所有文章的集合，用teacher obj的list来代替
        # 这里应该是对每一篇文章的处理
        data_temp_keys = input_sets[item_x].keys()  # key words of a file
        data_temp_pattern = input_sets[item_x]
        file_name = item_x  # name


        # data_temp_len = len(data_temp_keys) # 记录文档内词语的总数，这里改为pattern的总数
        # 这个len不对 ,这个是字典每个pattern的出现的数量已被记录了的
        sum_t = 0
        for temp_i in data_temp_keys:
            sum_t += data_temp_pattern[temp_i]
        data_temp_len = sum_t
        files_num += 1  # 文档数量加一
        for word in words:
            if word in data_temp_keys:  # 所有在这人的所有pattern，这个作为pattern只记录了key
                if not word in word_in_allfiles_stat:  # 如果这个word 在文档里面没出过
                    word_in_allfiles_stat[word] = 1  # 就把他加进去
                else:
                    word_in_allfiles_stat[word] += 1  # 如果出现过，则增加他出现的次数一次

                if not file_name in word_in_afile_stat:  # 字典，和下面的if一起处理
                    word_in_afile_stat[file_name] = {}
                if not word in word_in_afile_stat[file_name]:  # 添加元素，这个字典包括当前的文档的关键词的数量和当前文档的总词语的数量
                    word_in_afile_stat[file_name][word] = []
                    word_in_afile_stat[file_name][word].append(data_temp_pattern[word])#统计这个单词出现了几次
                    word_in_afile_stat[file_name][word].append(data_temp_len) # 总的数量
                    # word_in_afile_stat{a:{A:[aA,suma],B:[aB,suma],⋯⋯}, ⋯⋯}, b:{A:[bA,sumb],B:[bB,sumb],⋯⋯}, ⋯⋯},⋯⋯}
    if (word_in_afile_stat) and (word_in_allfiles_stat) and (files_num != 0):  # 如果这些都不为空的话
        TF_IDF_result = {}
        for filename in word_in_afile_stat.keys():
            TF_IDF_result[filename] = {}  # 当前的文件新建一个元素
            for word in word_in_afile_stat[filename].keys():  # 对于当前文档的关健词
                word_n = word_in_afile_stat[filename][word][0]  # 第一个表示a文档里面词语A的数量aA
                word_sum = word_in_afile_stat[filename][word][1]  # 第二个表示文档a里面的词语的总数
                with_word_sum = word_in_allfiles_stat[word]  # 这个词语出现的次数
                # 这里log后面的值太小了，但是如果样本的数量变大的话就没事了
                TF_IDF_result[filename][word] = ((word_n / word_sum)) * (math.log10(files_num /(with_word_sum+1)))  # tfidf的公式
                if if_weight:
                    TF_IDF_result[filename][word] *= words[word]  # multiply the times in the test set
        TF_IDF_total = {}
        for filename in TF_IDF_result.keys():
            print(TF_IDF_result[filename].values())
            TF_IDF_total[filename] = reduce(lambda x, y: x + y, TF_IDF_result[filename].values())  # 把每一值加起来
        result_temp = []
        result_temp = sorted(TF_IDF_total.items(), key=lambda x: x[1], reverse=True)  # 最后的结果按照从高到低返回
        result = result_temp
    else:
        result = ["None"]

    return result # result

# use to save the pattern for all the pattern
# a more regular method to save the data
# TODO(Zake Yao):it need to put in the tools.py
def dicSaver_rel(dic_t,label,save_path): # label应该是name
    json_str = json.dumps(dic_t)
    with open(save_path + str(label)+"_all.json","w") as json_file:
        json_file.write(json_str)

# use to clean the dic when the show time is less than show_times
# it is the regular method to delete the members,and the next one is for the test teacher
# return the new dic
def patterncleaner(dict, show_times):
    dic_temp = dict.copy()
    for key in dict:
        if (dic_temp[key]) <= show_times:
            if dic_temp[key] < show_times:
                print("Error! The times in score is less 1,and you can't minus 1")
            if dic_temp[key] == show_times:
                dic_temp.pop(key)
    return dic_temp

# use to sum the length : times of the pattern dic
def timecounter(dic_t):
    dic_count ={}
    for item in dic_t:
        if int(dic_t[item]) == 2:
            if 2 not in dic_count:
                dic_count[2] = 1
            else:
                dic_count[2] +=1
        elif int(dic_t[item]) == 3:
            if 3 not in dic_count:
                dic_count[3] = 1
            else:
                dic_count[3] +=1
        elif int(dic_t[item]) == 4:
            if 4 not in dic_count:
                dic_count[4] = 1
            else:
                dic_count[4] +=1
        elif int(dic_t[item]) == 5:
            if 5 not in dic_count:
                dic_count[5] = 1
            else:
                dic_count[5] +=1
        elif int(dic_t[item]) == 6:
            if 6 not in dic_count:
                dic_count[6] = 1
            else:
                dic_count[6] +=1
        elif int(dic_t[item]) == 7:
            if 7 not in dic_count:
                dic_count[7] = 1
            else:
                dic_count[7] +=1
        elif int(dic_t[item]) == 8:
            if 8 not in dic_count:
                dic_count[8] = 1
            else:
                dic_count[8] +=1
        else:
            if 10 not in dic_count:
                dic_count[10] = 1
            else:
                dic_count[10] +=1
    return dic_count
#count
def timecounter_v2(dic_t):
    dic_count ={}
    for item in dic_t:
        if len(item) == 2:
            if 2 not in dic_count:
                dic_count[2] = 1
            else:
                dic_count[2] +=1
        elif len(item) == 3:
            if 3 not in dic_count:
                dic_count[3] = 1
            else:
                dic_count[3] +=1
        elif len(item) == 4:
            if 4 not in dic_count:
                dic_count[4] = 1
            else:
                dic_count[4] +=1
        elif len(item) == 5:
            if 5 not in dic_count:
                dic_count[5] = 1
            else:
                dic_count[5] +=1
        elif len(item)== 6:
            if 6 not in dic_count:
                dic_count[6] = 1
            else:
                dic_count[6] +=1
        elif len(item) == 7:
            if 7 not in dic_count:
                dic_count[7] = 1
            else:
                dic_count[7] +=1
        elif len(item) == 8:
            if 8 not in dic_count:
                dic_count[8] = 1
            else:
                dic_count[8] +=1
        else:
            if 10 not in dic_count:
                dic_count[10] = 1
            else:
                dic_count[10] +=1
    return dic_count
# use to delete the include shorter pattern
# it's for the normal dic instead of another eachsmallpt
def shortptdeleter_rel(dic_t):
    dic_tempt = dic_t.copy()
    for key_t in dic_t:
        if key_t[0:-1] in dic_tempt:
            dic_tempt = eachsmallpt_rel(key_t[0:-1],dic_tempt)
    return dic_tempt.copy()


# 用于递归
def eachsmallpt_rel(key_t,dic_t):
    dic_temp = dic_t.copy()
    if key_t[0:-1] in dic_temp:
            dic_temp = eachsmallpt_rel(key_t[0:-1],dic_t)
    else:
        dic_temp.pop(key_t)
    return dic_temp.copy()

# use to sort the dic#这个只能按照可以的排序
def order_dic(dic_t):
    dic_temp = dic_t.copy()
    dic_sort = {}
    dic_sort = collections.OrderedDict(sorted(dic_temp.items(), key=lambda t: t[0]))
    return dic_sort
# use to sort the dic use value#这个只能按照可以的排序,从大到小
def order_dic_val(dic_t):
    dic_temp = dic_t.copy()
    dic_sort = {}
    dic_sort = collections.OrderedDict(sorted(dic_temp.items(), key=lambda t: t[1],reverse = True))
    return dic_sort

# use to do the cross validation in
# 感觉可以设定成，两个文件夹里，分别打开进行赋值然后和测试的结果对比
def cross_validation_onetime(pos_path,neg_path):
    pass

# use to rewrite the original action sequence, use the method of Kojima
# ckeek the method in https://www.oit.ac.jp/is/~sano/server/data/master/2018/kojima_presen.pdf
# page 9
def actionrewriter(list_t):
    cheek_seq =["", "", ""]  # the initial is 3 none
    list_n = []  # the new list
    for item in list_t:
        if item :
            cheek_seq.append(item)
            # cheek it with 4 elements in it
            if "" in cheek_seq:
                cheek_seq.pop(0)
                continue  # jump to the next step
            else:
                # choose the most one
                counter_seq = 0
                act_t =""  # if the counter is the same the first one will be outputed
                for x in cheek_seq:  # count each action in the seq
                    counter_t = cheek_seq.count(x)
                    if counter_t > counter_seq:
                        act_t = x
                        counter_seq = counter_t
                list_n.append(act_t)  # add the most one or the first one with the same counter
            # pop the fist one
            cheek_seq.pop(0)
    return  list_n

def sumup(dit):
    sum_t = 0
    for c in dit:
        sum_t+=dit[c]
    return  sum_t