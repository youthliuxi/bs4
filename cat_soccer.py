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

def insert(x_id,x):
	conn = mysql.connector.connect(user='root', password='', database='cat_soccer') 
	cursor = conn.cursor()


	html = getHtml("http://www.qiuduoduo.cn/scoreboard/%s" % (x))
	# print(html)
	# 下方的soup会自动解码
	soup = BeautifulSoup(html,"html.parser")
	# print(soup)
	div = soup.select('div[class="scoreboard"]')

	for div_html in div:
		# print(div_html)
		tr = div_html.select('tr')
		test_id = 0
		for tr_html in tr:
			test_id += 1
			if test_id < 3:# 排除前两行tr的干扰
				continue
			# print(tr_html)
			# print("\n")
			td = tr_html.select('td')
			text = []
			test_id += 1
			for td_html in td:
				# print(td_html.get_text().strip())
				text.append(td_html.get_text().strip())
			query = "insert into `soccer_team_sum`(`league_soccer`, `team_ranking`, `team`, `session`, `win`, `ping`, `negative`, `goal_fumble`, `point`) values (%s,%s,\"%s\",%s,%s,%s,%s,\"%s\",%s);" % (x_id,text[0],text[1],text[2],text[3],text[4],text[5],text[6],text[7])
			# print(query)
			cursor.execute(query)
			conn.commit()
			# print(text[0])

	cursor.close()
	conn.close()
	print("%sdone" % (x))
# CREATE TABLE `league_soccer_matches` (
#   `id` int(11) NOT NULL,
#   `name` char(20) NOT NULL,
#   `abbr` char(20) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# CREATE TABLE `soccer_team_sum` (
#   `id` int(11) NOT NULL,
#   `league_soccer` int(11) NOT NULL,
#   `team_ranking` int(11) NOT NULL,
#   `team` char(20) NOT NULL,
#   `session` int(11) NOT NULL,
#   `win` int(11) NOT NULL,
#   `ping` int(11) NOT NULL,
#   `negative` int(11) NOT NULL,
#   `goal_fumble` char(20) NOT NULL,
#   `point` int(11) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	

if __name__ == '__main__':
	league_soccer = [["英超","EPL"],["中超","CSL"],["西甲","Spanish"],["德甲","Bundesliga"],["意甲","Seria"],["法甲","Marseille"]]
	for x_id in range(0,6):
		insert(x_id+1,league_soccer[x_id][1])