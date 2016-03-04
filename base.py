import re
import json
import smtplib
from time import sleep

import requests
from bs4 import BeautifulSoup

from .models import *


class CrawlerException(Exception):
    """This is a base Exception for Crawler class."""


class LoginException(CrawlerException):
    pass


class UserNotExist(LoginException):
    pass


class PasswordMismatch(LoginException):
    pass


class RetryFail(CrawlerException):
    pass


class TaskException(Exception):
    pass


def retry_when_fail(act, attempt=3, interval=1):
    def _act(*args, **kargs):
        nonlocal attempt, interval
        for i in range(attemp):
            sleep(inerval)
            try:
                ret = act(*args, **kargs)
            except:
                continue
            finally:
                return ret
        raise RetryFail
    return _act


class Crawler(object):
    def __init__(self):
        self._root_url = "http://www.zhihu.com/"
        self._cookies = {}
        self._session = requests.Session()
        self.has_logged = False
    
    @property
    def cookies(self):
        return self._cookies
        
    @property
    def session(self):
        return self._session
    
    def login(self):
        r = self._session.get(self._root_url)
        soup = BeautifulSoup(r.content, "lxml")
        xsrf = soup.find("input", {"name":"_xsrf"}).get("value")
        r = self._session.post(self._root_url+"login/email", {
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
    
    @retry_when_fail
    def get_topic(self, id):
        r = self._session.get(_root_url+"topic/"+str(id))
        return None
    
    @retry_when_fail
    def get_question(self, id):
        pass
    
    @retry_when_fail
    def get_anwswer(self, id):
        pass
    
    @retry_when_fail     
    def get_user(self, id):
        pass
        

class Task(object):
    def __init__(self):
        self.queue = [] #todo: something should replace the list
    
    def add(self):
        pass