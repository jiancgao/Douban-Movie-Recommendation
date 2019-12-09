# coding: utf-8

from Project.cookie import douban_cookie
from bs4 import BeautifulSoup
import time
import MySQLdb
from datetime import datetime
# import uniout
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class following_spider(object):
    def __init__(self):
        self.opener = douban_cookie()
 
    def following_crawl(self, following_id_list, url, next_url):
        response = self.opener.open(next_url, timeout=180)
        res = response.read()
        soup = BeautifulSoup(res, 'html.parser')
        article = soup.find('div', class_ = 'article')
        lists = article.find_all('dd')
        # find all the following user's name for each user, append to a list
        if len(lists) != 0:
            for li in lists:
                nam = li.find('a')['href']
                u_name = nam.split('/')[4]
                following_id_list.append(u_name)
        else:
            print 'This man did not follow anybody.'
            return following_id_list, url
        return following_id_list, next_page
    
    
    def get_id_name(self, sql):
        sql = 'select user_id, name from user'
        con = MySQLdb.connect(host = 'localhost',
                              user = 'root',
                              passwd = 'your password',
                              db = 'douban',
                              charset = 'utf8')
        with con:
            cur = con.cursor()
            cur.execute(sql)
            id_ = cur.fetchall()
        return id_


    def add_data(self, sql, data):
        con = MySQLdb.connect(host = 'localhost',
                              user = 'root',
                              passwd = 'your password',
                              db = 'douban',
                              charset = 'utf8')
        
        with con:
            cur = con.cursor()
            cur.execute(sql, data)
    
if __name__ == '__main__':
    
    spider = following_spider()
    data = spider.get_id_name()
    k = 1
 
    for i in data:
        following_id_list = []
        u_id = i[0]
        link = 'https://www.douban.com/people/'
        name = i[1]
        url = link + name + '/contacts'
        next_page = url
        n = 1
        while True:
            following_id_list, next_page = spider.following_crawl(following_id_list, url, next_page)
            if next_page == url:
                break

        #inserting the id_dis
        update_sql = "update user set following_id=%s where user_id=%s"
        distance_data = (str(following_id_list), u_id)
        spider.add_data(update_sql, distance_data)
        now = datetime.now()
        print 'Added user:%s data into DB:NO.%s out of %s. %s' % (name,k,len(data),now)
        if k%1 == 0:
            time.sleep(1)
        if k%3 == 0:
            time.sleep(2)
        k += 1
    print 'Mission complete: successfully inserted all data into the DB'
    
    
