# -*- coding: utf-8 -
import requests
from bs4 import BeautifulSoup as BS
import re
import smtplib
from email.mime.text import MIMEText
import datetime, time

# -- CONFIG -- #
# A = "Always"
pattern = re.compile(r'<div id="js-ho.*;}">(.*)<a href=".*>更多<', re.S)

site = "https://www.zhihu.com"
hdr = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Host': 'www.zhihu.com',
    'DNT': '1'
    }
user = {'account': '',
        'password': ''}
mail = {'addr': '',
        'pwd': ''}
times = 1
freq = 3600
path = r'E:\Downloads\zhic.txt'

# -- FUNCTIONALITY -- #
def login(site, user, hdr):
    account = user['account']
    login_type = 'email' if '@' in account else 'phone_num'
    session = requests.Session()

    def get_xsrf():
        soup = BS(session.get(site, headers=hdr, timeout=30).text)
        return soup.find('input', {'name': '_xsrf'}).get('value')

    msg = {'rememberme': 'y',
           '_xsrf': get_xsrf(),
           'password': user['password'],
           login_type: account}
    auth = "%s/login/%s" % (site, login_type)
    
    try:
        if session.post(auth, headers=hdr, data=msg, timeout=30).json()['r'] == 0:
            print("Authentication completed...")
        else:
            print("""Authentication failed.\n
                  Please check your configuration or contact the author.""")
    except:  # Further exception handling to be added here
            raise 

    return session

def fpl(session, url, path, hdr, times, freq):
    """A fetch-parse-loop"""
    
    def fetch():
        res = session.get(url, headers=hdr)    
        return BS(re.search(pattern, res.text).groups()[0])
        
    def parse(soup):
        # TBD
        items = soup.find_all('div', {'class': 'feed-main'})
        return "\r\n".join(str(i) for i in items)

    # Todo: compare and remove duplicate items
    with open(path, 'w', encoding='utf-8') as out:
        for i in range(times):
            out.write(parse(fetch()))
            if i < times-1:
                time.sleep(freq)

def zhiliao(path, mail):
    news = open(path, 'r', encoding='utf-8').read()
    smtp_server = smtplib.SMTP_SSL("smtp.qq.com", port=465, timeout=30)
    smtp_server.login(mail['addr'], mail['pwd'])

    msg = MIMEText(news)
    msg['Subject'] = "News @zhihu %s" % datetime.datetime.today()
    msg["From"] = msg["To"] = mail['addr']
    
    smtp_server.send_message(msg)
    print("Thy will be done in earth, as it is in heaven.")

# -- MAIN -- #
if __name__ == "__main__":    
    session = login(site, user, hdr)
    fpl(session, site, path, hdr, times, freq)
    zhiliao(path, mail)
