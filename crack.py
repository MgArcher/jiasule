#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: jiajia
@file: crack.py
@time: 2020/7/28 14:11
"""
import re

import execjs
import requests


url = 'http://www.gsxt.gov.cn/index.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}
response = requests.get(url, headers=headers)
jsluid_h = response.headers['Set-Cookie'].split('=')[1].split(';')[0]
data = response.text
js = re.findall('<script>(.*?)</script>', data)[0]
with open(r'jiasule.js', encoding='utf-8') as f:
    wc_js = f.read()
ctx = execjs.compile(wc_js)
jsl_cookie = ctx.call('jsl', js)
jsl_clearance = re.findall('=(.*?);', jsl_cookie)[0]
print(jsluid_h)
print(jsl_clearance)


####  test  ######
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Cookie": f"__jsluid_h={jsluid_h}; __jsl_clearance={jsl_clearance}"
}
response = requests.get(url, headers=headers)
print(response.text)
print(response)