# -*- coding: utf-8 -*-
import io
import sys
import os
import mysql.connector
import urllib2
import urllib
import MySQLdb
import HTMLParser
import json
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding("utf-8")
html_parser = HTMLParser.HTMLParser()
def getHtml(url):
	request = urllib2.Request(url)
	page = urllib2.urlopen(request)
	html = page.read()
	return html

def json2dict(data):
	data_dict = json.loads(data)
	# print(data_dict)
	return data_dict

def getNextUrl(url):
	data_dict = json2dict(getHtml(url))
	next_url = data_dict['paging']['next']
	return next_url

def getIsEnd(url):
	data_dict = json2dict(getHtml(url))
	is_end = data_dict['paging']['is_end']
	return is_end

def insert_author(author_id,author):
	select_author = "select `author` from `zhihu_author` where `author_id`='"+author_id+"';"
	# print(select_author)
	cursor.execute(select_author)
	results = cursor.fetchall()
	for row in results:
		if row[0]==author:
			continue
		else:
			insert_author_sql = "replace into `zhihu_author` values('"+bytes(author_id)+"','"+author+"') "
			cursor.execute(insert_author_sql)

def insert_article(url):
	data_dict = json2dict(getHtml(url))
	for x in range(0,len(data_dict['data'])):
		if data_dict['data'][x]['verb'] != "MEMBER_CREATE_ARTICLE":
			continue
		else:
			title_id = data_dict['data'][x]['target']['id']
			title = data_dict['data'][x]['target']['title']
			url = data_dict['data'][x]['target']['url']
			author_id = data_dict['data'][x]['target']['author']['id']
			author = data_dict['data'][x]['target']['author']['name']
			content = data_dict['data'][x]['target']['content']
			download_img(content)
			insert_author(author_id,author)
			insert_sql = "insert into `zhihu`(`title_id`, `title`, `url`, `author_id`, `author`, `content`) values('"+bytes(title_id)+"','"+MySQLdb.escape_string(title)+"','"+url+"','"+MySQLdb.escape_string(author_id)+"','"+MySQLdb.escape_string(author)+"','"+MySQLdb.escape_string(content)+"');"
			# print(insert_sql)
			cursor.execute(insert_sql)
			for x in range(1,5):
				update_sql = "update `zhihu` set content=replace(content,'https://pic"+str(x)+".zhimg.com','img');"
				cursor.execute(update_sql)
			conn.commit()
	return True
	# return content

def download_img(content):
	path = os.getcwd()
	new_path = os.path.join(path, 'img')
	if not os.path.isdir(new_path):
	    os.mkdir(new_path)

	new_path +='/'
	soup = BeautifulSoup(content,"html.parser")
	imgs = soup.find_all("img")
	# print(imgs)
	x = 0
	for img_src in imgs:
	    # print(img_src['src'])
	    img_url = img_src['src']
	    if len(img_url) > 0:
	        file_name = img_url.split('/')[-1]
	        urllib.urlretrieve(img_url, new_path + file_name)
	
	# print("done")
	
def first():
	html = getHtml("https://www.zhihu.com/people/jiang-zhen-yu-67-74/activities")
	soup = BeautifulSoup(html,"lxml")
	# print(soup)
	data_div = soup.find_all("script", id="js-initialData")
	# print(data_div)
	data = data_div[0].get_text()
	# print(data)
	data_decode = json2dict(data)
	# print(data_decode)
	next_url = data_decode["initialState"]['people']['activitiesByUser']['jiang-zhen-yu-67-74']['previous']
	print(next_url)
	while(True):
		print(insert_article(next_url))
		is_end = getIsEnd(next_url) #判断是否有下一页
		if is_end == False:	
			# 如果有，更新下一页url
			next_url = getNextUrl(next_url)
		else:
			print("end")
			break

# CREATE TABLE `zhihu` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `title_id` int(100) NOT NULL,
#   `title` char(100) NOT NULL,
#   `url` char(100) NOT NULL,
#   `author_id` char(100) NOT NULL,
#   `author` char(40) NOT NULL,
#   `content` text NOT NULL,
#   PRIMARY KEY ( id )
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# CREATE TABLE `zhihu_author` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `author_id` char(100) NOT NULL,
#   `author` char(40) NOT NULL,
#   PRIMARY KEY ( id )
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
if __name__ == '__main__':
	conn = mysql.connector.connect(user='root', password='', database='cat_note') 
	cursor = conn.cursor()
	first()
	cursor.close()
	conn.close()