import re
import json
import smtplib

import requests
from bs4 import BeautifulSoup


class CrawlerException(Exception):
    """This is a base Exception for Crawler class."""


class LoginException(CrawlerException):
    pass


class UserNotExist(LoginException):
    pass


class PasswordMismatch(LoginException):
    pass
    
    
class TaskException(Exception):
    pass


class Crawler(object):
    def __init__(self):
        self._root_url = "http://www.zhihu.com/"
        self._cookies = {}
        self.has_logged = False
    
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
        if r.json()["r"]==0:
            self.has_login = True
        else:
            raise LoginException
        return None

    def login_required(func):
        def _func(self, *args):
            if not self.has_logged:
                try:
                    self.login()
                except LoginException:
                    raise LoginException #todo: fix it later
            ret = func(self, *args)
            return ret
        return _func
        
    def get_topic(self, id):
        pass
        
    def get_anwswer(self, id):
        pass
        
    def get_user(self, id):
        pass
        

class Task(object):
    def __init__(self):
        self.queue = [] #todo: something should replace the list
    
    def add(self):
        pass