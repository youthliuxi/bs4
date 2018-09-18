# -*- coding: utf-8 -*-
import io
import sys
import mysql.connector
import urllib2 as urllib
import MySQLdb
import HTMLParser
import json
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding("utf-8")
html_parser = HTMLParser.HTMLParser()
def getHtml(url):
	request = urllib.Request(url)
	page = urllib.urlopen(request)
	html = page.read()
	return html

def json2dict(data):
	data_json = html_parser.unescape(data)
	data_dict = json.loads(data_json)
	return data_dict

def getNextUrl(url):
	data_dict = json2dict(getHtml(url))
	next_url = data_dict['paging']['next']
	return next_url

def getIsEnd(url):
	data_dict = json2dict(getHtml(url))
	is_end = data_dict['paging']['is_end']
	return is_end

def insert_article(url):
	data_dict = json2dict(getHtml(url))
	for x in range(0,len(data_dict['data'])):
		if data_dict['data'][x]['verb'] != "MEMBER_CREATE_ARTICLE":
			continue
		else:
			title_id = data_dict['data'][x]['target']['id']
			title = data_dict['data'][x]['target']['title']
			url = data_dict['data'][x]['target']['url']
			author = data_dict['data'][x]['target']['author']['name']
			content = data_dict['data'][x]['target']['content']
			insert_sql = "insert into `zhihu_old` values(0,'"+bytes(title_id)+"','"+MySQLdb.escape_string(title)+"','"+url+"','"+MySQLdb.escape_string(author)+"','"+MySQLdb.escape_string(content)+"');"
			# print(insert_sql)
			cursor.execute(insert_sql)
			conn.commit()
	return True

def first():
	html = getHtml("https://www.zhihu.com/people/jiang-zhen-yu-67-74/activities")
	soup = BeautifulSoup(html,"lxml")
	# print(soup)
	data_div = soup.find_all("div", id="data")
	data = data_div[0]
	data_decode = json2dict(data['data-state'])

	next_url = data_decode['people']['activitiesByUser']['jiang-zhen-yu-67-74']['previous']
	while(True):
		print(insert_article(next_url))
		is_end = getIsEnd(next_url) #判断是否有下一页
		if is_end == False:	
			# 如果有，更新下一页url
			next_url = getNextUrl(next_url)
		else:
			print("end")
			break


# CREATE TABLE `zhihu_old` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `title_id` int(100) NOT NULL,
#   `title` char(100) NOT NULL,
#   `url` char(100) NOT NULL,
#   `author` char(40) NOT NULL,
#   `content` text NOT NULL,
#   PRIMARY KEY ( id )
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

if __name__ == '__main__':
	conn = mysql.connector.connect(user='root', password='', database='cat_note') 
	cursor = conn.cursor()
	first()
	cursor.close()
	conn.close()