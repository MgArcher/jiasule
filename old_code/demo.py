#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: jiajia
@file: demo.py
@time: 2020/7/28 11:21
"""

import re

import execjs
import requests
from requests.utils import dict_from_cookiejar

headers = {
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36"
}
r = requests.get('http://www.gsxt.gov.cn/index.html', headers=headers)
cookie = dict_from_cookiejar(r.cookies)
print(cookie)
js = 'function jsl(){window = {navigator: {userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Geck' \
     'o) Chrome/83.0.4103.116 Safari/537.36"},outerWidth: 1920,outerHeight: 1050,};location = {reload:function () {' \
     '}};document = {};' + re.findall('<script>(.*?)</script>', r.text)[0] + ';return document.cookie}'
print(js)
ctx = execjs.compile(js)
jsl_cookie = ctx.call('jsl')
jsl_cookie = re.findall('=(.*?);', jsl_cookie)[0]
cookie.update({"__jsl_clearance": jsl_cookie})
r = requests.get('http://www.gsxt.gov.cn/index.html', headers=headers, cookies=cookie)
print(r.text)