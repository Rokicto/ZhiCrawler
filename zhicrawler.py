# -*- coding: utf-8 -
import requests
from bs4 import BeautifulSoup as BS
import re
import smtplib
from email.mime.text import MIMEText
import datetime

top_url = 'https://www.zhihu.com'
auth_url = top_url + "/login/phone_num" #
_header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Host': 'www.zhihu.com',
    'DNT': '1'
    }
_data = {
    'phone_num': '',
    'password': '',
    'rememberme': 'y'
    }

session = requests.Session()
_soup = BS(session.get(top_url, headers=_header, timeout=30).text)
_data['_xsrf'] = _soup.find('input', {'name': '_xsrf'}).get('value')
r_login = session.post(auth_url, headers=_header, data=_data, timeout=30)
if r_login.json()['r'] != 0:
    raise
pattern = re.compile(r'<div id="js-ho.*;}">(.*)<a href=".*>更多<', re.S)
res = session.get(top_url, headers=_header)
soup = BS(re.search(pattern, res.text).groups()[0])
feed_items = soup.find_all('div', {'class': 'feed-main'})

def item_parser(items):
    for i in items:
        source = item.find('a')
        question = item.find('a', {'class': 'question_link'})
    pass

_mail_addr, _pwd = "", ""
_mail_to = _mail_addr
msg = MIMEText("\r\n".join(str(i) for i in feed_items))
msg["Subject"] = "知了 %s" % datetime.datetime.today()
msg["From"], msg["To"] = _mail_addr, _mail_to
smtp = smtplib.SMTP_SSL("smtp.qq.com", port=465, timeout=30)
smtp.login(_mail_addr, _pwd)
smtp.send_message(msg)

#<div id="js-home-feed-list" class="zh-general-list clearfix" data-init="{&quot;params&quot;: {}, &quot;nodename&quot;: &quot;HomeFeedListV2&quot;}">
