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

from __future__ import division
import math
from functools import reduce



def TF_IDF_Compute(file_import_url, file_export_url, *words):
    data_source = open(file_import_url, 'r')
    data = data_source.readline()  # 读取一行 不需要读取行
    word_in_afile_stat = {}
    word_in_allfiles_stat = {}
    files_num = 0
    while (data != ""):  # 这个data应该是一个所有文章的集合，用teacher obj的list来代替
        # 这里应该是对每一篇文章的处理
        data_temp_1 = []
        data_temp_2 = []
        data_temp_1 = data.split("\t")  # file name and key words of a file
        data_temp_2 = data_temp_1[1].split(",")  # key words of a file
        file_name = data_temp_1[0]  # 记录文档名称 ，这里改为name
        data_temp_len = len(data_temp_2)  # 记录文档内词语的总数，这里改为pattern的总数
        files_num += 1  # 文档数量加一
        for word in words:  # ？
            if word in data_temp_2:  # 如果这个单词在这个文章里面
                if not word in word_in_allfiles_stat:  # 如果这个word 在其他的文档里面没出过
                    word_in_allfiles_stat[word] = 1  # 就把他加进去
                else:
                    word_in_allfiles_stat[word] += 1  # 如果出现过，则增加他出现的次数一次

                if not file_name in word_in_afile_stat:  # 字典，和下面的if一起处理
                    word_in_afile_stat[file_name] = {}
                if not word in word_in_afile_stat[file_name]:  # 添加元素，这个字典包括当前的文档的关键词的数量和当前文档的总词语的数量
                    word_in_afile_stat[file_name][word] = []
                    word_in_afile_stat[file_name][word].append(data_temp_2.count(word))
                    word_in_afile_stat[file_name][word].append(data_temp_len)
        data = data_source.readline()  # 读取下一行，这个方法可以，可以有时候可以处理最后第一次处理的时候的问题
    data_source.close()  # 最后把文本关闭

    if (word_in_afile_stat) and (word_in_allfiles_stat) and (files_num != 0):  # 如果这些都不为空的话
        TF_IDF_result = {}
        for filename in word_in_afile_stat.keys():
            TF_IDF_result[filename] = {}  # 当前的文件新建一个元素
            for word in word_in_afile_stat[filename].keys():  # 对于当前文档的关健词
                word_n = word_in_afile_stat[filename][word][0]  # 第一个表示a文档里面词语A的数量aA
                word_sum = word_in_afile_stat[filename][word][1]  # 第二个表示文档a里面的词语的总数
                with_word_sum = word_in_allfiles_stat[word]  # 这个词语出现的次数
                TF_IDF_result[filename][word] = ((word_n / word_sum)) * (
                    math.log10(files_num / with_word_sum))  # tfidf的公式
        TF_IDF_total = {}
        for filename in TF_IDF_result.keys():
            TF_IDF_total[filename] = reduce(lambda x, y: x + y, TF_IDF_result[filename].values())  # 把每一值加起来
        result_temp = []
        result_temp = sorted(TF_IDF_total.items(), key=lambda x: x[1], reverse=True)  # 最后的结果按照从高到低返回
        k = 20  # 需要查找多少人
        result = []
        for item in result_temp:
            if k != 0:
                result.append(item[0])
                k -= 1
            else:
                break
    else:
        result = ["None"]
    # if out_to_file:  # 是否需要输出为txt
    #     export = open(file_export_url, 'w')
    #     for item in result:
    #         export.write(item + '\n')
    #     export.close()
    # else:
    return result