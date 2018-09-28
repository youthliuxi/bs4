## 声明

&emsp;&emsp;本代码只用于个人批量保存学习资料，供本人在电脑无法联网的情况下可以翻阅，其中不包含任何商业行为以及不对文章进行任何性质的转载

## 简介

&emsp;&emsp;使用beautiful soup 4分别抓取知乎专栏文章、csdn、imooc笔记，保存到mysql中

## 说明

### 非py格式

&emsp;&emsp;所有非py格式文件均为某单一样本，用来做某一功能的测试样本使用

### csdn_note.py

&emsp;&emsp;抓取保存csdn某用户的文章

&emsp;&emsp;未解决问题：csdn存在图片防盗链

### imooc_note.py

&emsp;&emsp;抓取imooc某用户文章保存到本地，属于第一个熟悉beautifulsoup的项目，各种语句均是不断尝试后确定下来的

### imooc_note_N_g_t.py

&emsp;&emsp;与上一个不同的是，抓取正文时不使用get_text()函数，而是直接进行utf-8解码

### zhihu_and_img.py

&emsp;&emsp;该文件已经完成了将某用户发表的所有知乎文章存入数据库，同时将其所有图片下载到img文件夹下

&emsp;&emsp;同时还做到了将正文中的图片url路径修改为本地相对路径img

&emsp;&emsp;与之相匹配的还有一套php代码用来读取数据库中的文件并粗略的展示出来

&emsp;&emsp;改进目标：添加一个数据表，保存作者信息，这样可以双表联合查询，同时将代码改造成能够保存知乎任意用户文章的代码

### zhihu_old.py

&emsp;&emsp;该文件是最初的抓取文件，只讲文章原始信息抓取出来，并未添加img下载和图片路径替换代码，数据库结构也略有差异