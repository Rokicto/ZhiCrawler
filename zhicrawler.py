# -*- coding: utf-8 -
import requests
from bs4 import BeautifulSoup as BS
import re
import smtplib
from email.mime.text import MIMEText
import datetime, time
import yaml

# -- config -- #
with open(r'./yaml') as f:
    config = yaml.load(f)
    
pattern = re.compile(config['pattern'], re.S)

# -- FUNCTIONALITY -- #
def login(site, user, hdr):
    account = str(config['user']['account'])
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

    msg = MIMEText(news)
    msg['Subject'] = "News @zhihu %s" % datetime.datetime.today()
    msg["From"] = msg["To"] = mail['addr']

    target = "smtp.%s" % mail['addr'].split("@")[1]
    smtp_server = smtplib.SMTP_SSL(target, port=465, timeout=30)
    smtp_server.login(mail['addr'], mail['pwd'])

    
    smtp_server.send_message(msg)
    print("Thy will be done in earth, as it is in heaven.")

# -- MAIN -- #
if __name__ == "__main__":    
    session = login(*(config[i] for i in ('site', 'user', 'hdr')))
    fpl(session, *(config[i] for i in 'site, path, hdr, times, freq'.split(', ')))
    zhiliao(*(config[i] for i in ('path', 'mail')))
