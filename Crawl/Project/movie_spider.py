# coding: utf-8

import urllib2
import json
import MySQLdb
# import uniout
import sys
import time
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def movie_spider(url, number):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
    hdr = {'User-Agent' : user_agent,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connection': 'keep-alive'} 
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    res = response.read()
    lists = json.loads(res)
    data = ()
    try:
        rate = lists[u'rating'][u'average']
        data += (rate,)
    except:
        data += ('None',)
    try:
        year = lists[u'year']
        data += (year,)
    except:
        data += ('None',)
    try:
        types = lists[u'genres']
        ty = ''
        for t in types:
            ty += t + ','
        ty = ty[:-1]
        data += (ty,)
    except:
        data += ('None',)
    try:
        actor = lists[u'casts']
        actors = ''
        for a in actor:
            actors += a[u'name'] + ','
        actors = actors[:-1]
        data += (actors,)
    except:
        data += ('None',)
    try:
        countries = lists[u'countries'][0]
        data += (countries,)
    except:
        data += ('None',)
    try:
        summary = lists[u'summary']
        data += (summary,)
    except:
        data += ('None',)
    try:
        directors = lists[u'directors'][0][u'name']
        data += (directors,)
    except:
        data += ('None',)
    data += (number,)
#     movies = []
#     for l in lists:
#         title = l['title'].encode('utf-8')
#         movie = (l['rate'], title, l['url'], l['id'])
#         movies.append(movie)
#     print rate,'\n',year,'\n',ty,'\n',actors,'\n',countries,'\n',summary,'\n',directors,'\n'
#     print data,len(data)
    return data


def data_insert(sql,data):
    con = MySQLdb.connect(host = 'localhost',
                          user = 'root',
                          passwd = 'your password',
                          db = 'douban',
                          charset = 'utf8')
    
    with con:
        cur = con.cursor()
        cur.execute(sql,data)


def output(sql):
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

        
if __name__ == '__main__':
    sq = 'select number,id from movie'
    movies = output(sq)
    for n,movie in enumerate(movies):
        number = movie[0]
        id_ = movie[1]
        url = 'https://api.douban.com/v2/movie/subject/' +id_
        data = movie_spider(url, number)
        sql = 'update movie set rate=%s,year=%s,type=%s,actors=%s,countries=%s,summary=%s,directors=%s where number=%s'
        data_insert(sql, data)
        now = datetime.now()
        print 'Movie:%s is finished: %s out of %s. %s' % (id_,n+1,len(movies),now)
        if (n+1)%1 == 0:
            time.sleep(8)
    
    
    
    
    