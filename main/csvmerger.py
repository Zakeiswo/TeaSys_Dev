# -*- coding: utf-8 -*-
#!/usr/bin/python3.7
import os
import re
def sort_key(s):
	if s:
		try:
			c = re.findall('[0-9]+', s)[0]#通过正则表达式匹配中间的数字部分
		except:
			c = -1
		return int(c)
def strsort(alist):
	alist.sort(key=sort_key,reverse=False)# 从小到大的顺序
	return alist

path ="/Users/syao/desktop/res/score_result/"
line_list =[]
if not os.path.exists(path):
	print("Fiile can't find")
	exit()
files = os.listdir(path)
files.sort()
files=strsort(files)  # 防止出现文件名里面10比2排在前面的情况
if ".DS_Store" in files:
	files.remove(".DS_Store")
sum_f = len(files)# 计算文件的总数
for f in files:
	i=0
	print(files)
	print(f)
	temp_path = os.path.join(path,f)
	w1 = open(temp_path,"r")
	lines = w1.readline()
	while lines:
		print(lines,end= '')
		#写入
		if f == files[0]:# 因为sort过
			line_list.append(lines)
		else:
			temp_line = lines.replace('\n', '').split(",")
			print(temp_line)
			temp_line_string = ","+temp_line[2]+","+temp_line[3]+","+temp_line[4]+","+temp_line[5]+"\n"
			line_list[i]=line_list[i].replace('\n', '')+temp_line_string
		#更新
		i+=1
		lines = w1.readline()
	w1.close()
with open("/Users/syao/desktop/res/all_result"+".csv","w+") as fff:#写入到一个csv的里面
	fff.writelines(line_list)
print("Done!!!")