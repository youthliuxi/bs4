# -*- coding: utf-8 -*-
import io
import sys
import mysql.connector
import urllib2 as urllib
import MySQLdb
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding("utf-8")
def getHtml(url):
	request = urllib.Request(url)
	page = urllib.urlopen(request)
	html = page.read()
	return html

def getArticle(title_url):
	article_html = getHtml(title_url).decode('utf-8')
	article_soup = BeautifulSoup(article_html,"lxml")
	# print(article_soup.prettify())
	article_title = article_soup.find_all('span', class_="d-t")
	insert_title = article_title[0].get_text()
	article_author = article_soup.find_all('a', class_="nick")
	insert_author = article_author[0].get_text()
	article_content = article_soup.find_all('div', class_="detail-content")
	insert_content = article_content[0].get_text()
	return [insert_title,insert_author,insert_content]

def insert(x):
	conn = mysql.connector.connect(user='root', password='', database='cat_note') 
	cursor = conn.cursor()

	html = getHtml("https://www.imooc.com/u/3931598/articles?page=%d" % (x))

	# print(html.decode('utf-8'))]
	# 下方的soup会自动解码
	soup = BeautifulSoup(html,"lxml")
	# print(soup.find("a", class_="title-detail"))
	a = soup.find_all("a", class_="title-detail")
	for link in a:
		a_href = link.get("href")
		# print(a_href)
		title_url = "https://www.imooc.com" + a_href
		# print(title_url)
		
		insert_title,insert_author,insert_content = getArticle(title_url)
		query = "insert into `imooc_note` values(0,'"+MySQLdb.escape_string(insert_title)+"','"+MySQLdb.escape_string(insert_author)+"','"+MySQLdb.escape_string(insert_content)+"');"
		# print(query)
		cursor.execute(query)
		conn.commit()

	cursor.close()
	conn.close()
	print("%ddone" % (x))
	# CREATE TABLE `csdn_note` (
	#   `id` int NOT NULL AUTO_INCREMENT,
	#   `title` char(100) NOT NULL,
	#   `author` char(40) NOT NULL,
	#   `content` text NOT NULL,
	#   PRIMARY KEY ( id )
	# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	# 

if __name__ == '__main__':
	for x in range(1,12):
		insert(x)
	# insert_title,insert_author,insert_content = getArticle("https://www.imooc.com/article/46859")
	# # print(insert_content)
	# query = "insert into `imooc_note` values(0,'"+insert_title+"','"+insert_author+"','"+str(insert_content)+"');"
	# print(query)