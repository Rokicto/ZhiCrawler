import re
import json
import smtplib

import requests
from bs4 import BeautifulSoup

from . import settings

__all__ = ["Crawler"]

class Crawler(object):
    def __init__(self):
        self._root_url = "http://www.zhihu.com/"
        self._cookies = {}
    
    def login(self):
        r = requests.get(self._root_url)
        soup = BeautifulSoup(r.content, "lxml")
        xsrf = soup.find("input", {"name":"_xsrf"}).get("value")
        r = requests.post(self._root_url+"login/email", {
            "_xsrf": xsrf,
            "email": settings.SPIDER_ACCOUNT,
            "password": settings.SPIDER_PASSWORD,
            "remeber_me": True,
            })
        self._cookies.update(r.cookies)
        return None

    def login_required(func):
        def _func(*args):
            ret = func(*args)
            return ret
        return _func
        
    def something(self):
        pass
        