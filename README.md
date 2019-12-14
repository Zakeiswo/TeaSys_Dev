<h1 align="center">Welcome to TeaSys_Dev 👋</h1>
<p>
  <img src="https://img.shields.io/badge/version-0.9.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/Zakeiswo/TeaSys_Dev#readme">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/kefranabg/readme-md-generator/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" target="_blank" />
  </a>
  <a href="https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
</p>

> Use for st-gcn to build a system which is used to compute the score of a teacher's actions in a class.


### 🏠 [Homepage](https://github.com/Zakeiswo/TeaSys_Dev#readme)

## Intruduction
This project is used to compute the score of the a teacher action  in a class. You can use the video data as the input, the output of it is the score and the video(Optional).<br/>


## Before start
You have to use the St-gcn-tea which base on the [St-gcn](https://github.com/yysijie/st-gcn)  to get the action sequeues.<br/>
You can download the St-gcn-tea in the page：[St-gcn-tea](https://drive.google.com/file/d/1dFLiBchhfdvJpKcDVh7KYeu4B6jVx8qm/view?usp=sharing). <br/>
The path of the video need to be changed.<br/>
In fact, the input of video can be too big to deal with. With the 8GB RAM and GTX1080，I can deal with around 4 minutes
320x180 video one time. 
I have write the a file to deal with this situation, which cut the video into 4 minutes clips and put them into the st-gcn-tea.<br/>
However, you must **change the path of the code** to apply to your own computer environment.<br/>
You can get the csv or json data from the St-gcn-tea when you use the video as the input.<br/>
Run the St-gcn-tea by this command:
```sh
Python3 batch_stgcn_plus.py
```
*The viewpoint of the video you used have to be the front of the blackboard.


## 

## Prerequisites
Python >=3.0<br />

python package:<br />
fuzzywuzzy >=0.17.0


## Run
When you want use this project you have to get the csv data of the video from the St-gcn-tea first.<br/>
Than you have change the path of the data in main function.
>About my code , there are 2 parts of the process, first part is used to deal with the original data
the next is using the processed data to compute the score.
>>In the first part , you have to build the Object of ProTeacher and NewTeacher class to deal with the dat. 
This part only need to run when the new data come. The next time you can comment out the code of this part.<br/>
Class NewTeacher is also the same way.You can use this code to build and deal with the new data:
```
prot = ProTeacher(<Name of the teacher>, <The path of the data>, <The path to save the processed data>)
prot.pfdicSaver()
```
>> The next part you is about the score computation.<br/>
≥≥First, you need to build a object of TestTeacher
```python
t = TestTeacher(<Name>, <The path of data>)
```
>>Than you have to read the processed data 
```python
t.jsonReader_pf_onetime(<The path of the processed data>,<Name>,<0 or 1 ,when o means new and 1 means pro >)
```
>>Then you need use this code to delete the common patterns:
```python
t.dicCommonDeleteOnetime() 
```
>>Then you should use this code to compress the data from 4~8 results into 1 action. 
Also you can change the 4~8 to another range :
You can choose to use kojima function or not.<br/>
When use Kojima function:
```python
 t.compressList_id_t(main.tools.actionrewriter(t.ac_list_ori), 4, 8)
```
>>Without Kojima function:
```python
 t.compressList_id_t(t.ac_list_ori, 4, 8)
```
>>Then we use this code to matching the patterns in the new and pro dataset:
```python
t.patternCheeker(maxlen)
```
>>Next, use this code to delete the pattern when the matching times is one. You can change the parameter 
if you want to delete the the matching times is more than one:
```
t.patterncleanerfortesttea(<Matching times, eg.1>)
```
>>Then you can use this code to output the score:
```
print(t.scorecalculater_ave())
```
>>If you want to get the visualized video, you can use this code to get the JSON file 
for creating the video:
```
t.visualization(<Path to save the JSON file>,t.name)
```
After  changing  the main function, you can run the project by this commend:

```sh
python3 testteacher.py
```
## Visualization 
If you want to get the result of video ,you can download the demo of my video maker:
[st-gcn-video](https://drive.google.com/file/d/1BxsygKbjDBekqqZUlOC3nCP1Vtq0v_SD/view?usp=sharing)<br/>
You need change the path of the JSON file in demo.py in this video maler and than run
the code by this comment:<br/>
```sh
python3 demo.py
```
*Attention the RAM of my computer is 16GB, the resolution of video I used is 320×180,
time of the video is around 20 minutes.
## Author

👤 **Zake(Yao Shunyu)**

* Github: [@Zakeiswo](https://github.com/Zakeiswo)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/kefranabg/readme-md-generator/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Zake(Yao Shunyu)](https://github.com/Zakeiswo).<br />
This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
