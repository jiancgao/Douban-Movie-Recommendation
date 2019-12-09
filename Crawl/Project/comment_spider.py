# coding: utf-8

from Project.cookie import douban_cookie
from Project.movie_spider import output
import uniout
from bs4 import BeautifulSoup
import sys
import MySQLdb
import time
from datetime import datetime
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class comment_spider(object):
    def __init__(self):
        self.opener = douban_cookie()

    def crawl(self, comment, u_id, url, next_url):
#         try:
        response = self.opener.open(next_url, timeout=180)
        res = response.read()
        soup = BeautifulSoup(res, 'html.parser')
        article = soup.find('div', class_ = 'article')
        lists = article.find('div', class_='grid-view').find_all('div', class_='info')
        try:
            for li in lists:
                nam = li.find('a')['href']
                m_id = nam.split('/')[4]
                try:
                    com = li.find('span', class_='comment').text
                    comment[m_id] = com
                except:
                    print 'This man did not give his comment about this movie.'
            new_url = article.find('div', class_ = 'paginator')
            next_page = new_url.find('link', rel = 'next')['href']
        except:
            return comment, url
        return comment, next_page
    
    def get_id_url(self):
        sql = 'select user_id, name from user'
        data = output(sql)
        return data

    def add_data(self, sql, data):
        con = MySQLdb.connect(host = 'localhost',
                              user = 'root',
                              passwd = 'your password',
                              db = 'douban',
                              charset = 'utf8')
        
        with con:
            cur = con.cursor()
            cur.execute(sql, data)

    def filter_emoji(self, desstr, restr=''):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

if __name__ == '__main__':
    
    spider = comment_spider()
    data = spider.get_id_url()
    k = 1

    for i in data:
        comment = {}
        u_id = i[0]
        link = 'https://movie.douban.com/people/'
        name = i[1]
        url = link + name + '/collect?start=0&sort=time&rating=all&filter=all&mode=grid'
        next_page = url
        n = 1
        while n<11:
#             print 'next_page: ' + next_page
            comment, next_page = spider.crawl(comment, u_id, url, next_page)
            print 'Crawling the No.%s page of user: %s id:%s is finished' % (n, name, u_id)
            if next_page == url:
                break
            if n%1 == 0:
                time.sleep(2)
            if n%5 == 0:
                time.sleep(2)
            n += 1
        if k%3 == 0:
            time.sleep(1)
#         print comment

        #inserting the comment
        comments = '{'
        for key,values in comment.items():
            comments += key + ':' + values + ','
        comments = comments[:-1] + '}'
        comments = spider.filter_emoji(comments)
        update_sql = "update user set comments=%s where user_id=%s"
        comment_data = (comments, u_id)
        spider.add_data(update_sql, comment_data)
        now = datetime.now()
        print 'Added user:%s data into table:rate. NO.%s out of %s. %s' % (name, k, len(data),now)
        k += 1
    print 'Mission complete: successfully inserted all data into the DB'
    
    
    
