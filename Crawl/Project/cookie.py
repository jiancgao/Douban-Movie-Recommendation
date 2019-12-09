# coding: utf-8
import cookielib
import urllib2
import urllib
from bs4 import BeautifulSoup

def douban_cookie():
    cookie= cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
#     proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0.1:51661'})
#     opener = urllib2.build_opener(proxy_support, handler, urllib2.HTTPHandler)
    opener = urllib2.build_opener(handler)
    post_url = 'https://accounts.douban.com/login'
    req = urllib2.Request(post_url)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    verify_url = soup.find('img', id='captcha_image')['src']
    verify_id = soup.find('input', {'name':'captcha-id'})['value']
    picture = opener.open(verify_url).read()
    local = open('e:/image.jpg', 'wb')
    local.write(picture)
    local.close()
    verify_code = raw_input('Please input the verify code： ')
    
    postdata = urllib.urlencode({'form_email':'your account',
                                 'form_password':'your password',
                                'captcha-id':verify_id,
                                'captcha-solution':verify_code})
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
    hdr = {'User-Agent' : user_agent,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connection': 'keep-alive'}  
    
    request = urllib2.Request(post_url, postdata, headers=hdr)
    response = opener.open(request)
    print 'Login successfully!'
    return opener



