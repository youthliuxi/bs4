# -*- coding: utf-8 -*-
import io
import sys
import mysql.connector
import urllib2 as urllib
import MySQLdb
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
def getHtml(url):
	request = urllib.Request(url)
	page = urllib.urlopen(request)
	html = page.read()
	return html

def getArticle(title_url):
	article_html = getHtml(title_url).decode("utf-8")
	article_soup = BeautifulSoup(article_html,"html5lib")
	# print(article_soup.prettify())
	article_title = article_soup.find_all('h1', class_="title-article")
	insert_title = article_title[0].get_text()
	article_author = article_soup.find_all('a', class_="text-truncate")
	insert_author = article_author[0].get_text()
	article_content = article_soup.find_all('div', id="article_content")
	insert_content = article_content[0].encode("utf-8")
	return [insert_title,insert_author,insert_content]

def insert(x):
	conn = mysql.connector.connect(user='root', password='', database='cat_note') 
	cursor = conn.cursor()


	html = getHtml("https://blog.csdn.net/yunge812/article/list/%d" % (x))
	# print(html)
	# 下方的soup会自动解码
	soup = BeautifulSoup(html,"html.parser")
	# print(soup)
	h4 = soup.find_all('h4')
	i = 0
	for h4_html in h4:
		a_href = h4_html.a.get("href")
		i += 1
		if i < 2:
		# 之所以做此修改，是因为csdn小改动了版面，添加了一个“只看原创”的链接，和文章标题链接同格式
			continue
		# print(a_href)
		insert_title,insert_author,insert_content = getArticle(a_href)
		# print(insert_content)
		query = "insert into `csdn_note` values(0,'"+MySQLdb.escape_string(insert_title)+"','"+MySQLdb.escape_string(insert_author)+"','"+MySQLdb.escape_string(insert_content)+"');"
		# print(query)
		cursor.execute(query)
		conn.commit()
		# break

	cursor.close()
	conn.close()
	print("%ddone" % (x))
	# CREATE TABLE `imooc_note` (
	#   `id` int NOT NULL AUTO_INCREMENT,
	#   `title` char(100) NOT NULL,
	#   `author` char(40) NOT NULL,
	#   `content` text NOT NULL,
	#   PRIMARY KEY ( id )
	# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	

if __name__ == '__main__':
	for x in range(1,4):
		print(x)
		insert(x)
	# insert_title,insert_author,insert_content = getArticle("https://www.imooc.com/article/46859")
	# # print(insert_content)
	# query = "insert into `imooc_note` values(0,'"+insert_title+"','"+insert_author+"','"+str(insert_content)+"');"
	# print(query)