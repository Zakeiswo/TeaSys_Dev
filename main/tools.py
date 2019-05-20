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

