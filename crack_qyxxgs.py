# encoding: utf-8
"""
!/usr/bin/python3
@File: crack.py
@Author:jiajia
@time: 2019/4/30 11:15
"""
import re
import time

import execjs
import requests


class Crack(object):
    """
    同一ip频繁使用：
        出现正常200但是没有结果
        第一次解密出来是错误的
    """
    def __init__(self, url, test_url):
        with open(r'wc_js.js', encoding='utf-8') as f:
            wc_js = f.read()
        self.wc_js = execjs.compile(wc_js)
        self.url = url
        self.test_url = test_url

        # 固定user_agent,后台使用user-agent验证cookies, 之后的访问也需要使用这个
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }

    def acquire_js(self):
        """
        不带cookies请求首页，获得返回的js
        :return:页面中的js,和set_cookies中的jsluid
        """
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 521:
            return response.text, response.headers['Set-Cookie'].split('=')[1].split(';')[0]
        else:
            print(response.text)
            print(self.headers)
            return None, None

    def first_decryption(self, first_js):
        """
        解密js,获得第二层加密的js
        :param first_js:
        :return:
        """
        x = re.findall('var x="(.*?)"', first_js)[0]
        y = re.findall(',y="(.*?)"', first_js)[0]
        second_js = self.wc_js.call('once_js', x, y)
        # second_js = self.wc_js.call('get_js', x, y, z)
        return second_js

    def regex(self, js):
        regex =  "!*window\[.*?\]"
        find = re.findall(regex, js)
        if find:
            for f in find:
                if '!' in f:
                    if len(re.findall('!', f)) % 2 == 0:
                        js = js.replace(f, 'false')
                    else:
                        js = js.replace(f, 'true')
                else:
                    js = js.replace(f, 'undefined')
        js = js.replace('window.headless', 'undefined')
        return js

    def replace_url(self, js):
        # 替换1
        # 取出两个变量名
        _3d = re.findall("(var .{0,5}=)document\.createElement\('div'\);", js)
        _2b = re.findall("(var .{0,5}=).{0,5}\.match\(/https\?:\\\/\\\//\)\[0\];", js)

        # 替换成要访问的url
        js = re.sub("var .{0,5}=document\.createElement\('div'\);", _3d[0] + f'"{self.url.replace("http://", "")}";',
                    js)
        js = re.sub("_.{0,5}\.innerHTML='<a href=.{0,25}</a>';", "", js)
        js = re.sub("_.{0,5}=.{0,5}\.firstChild\.href;", "", js)
        js = re.sub("var .{0,5}=.{0,5}\.match\(/https\?:\\\/\\\//\)\[0\];", _2b[0] + '"http://";', js)
        js = re.sub("_.{0,5}=.{0,5}\.substr\(.{0,5}\.length\)\.toLowerCase\(\);", "", js)
        return js

    def second_decryption(self, second_js):
        """
        把第二层js准换成本地可以运行的js
        !!!此处可能会出错!!!
        :param second_js: 第一次解密的js
        :return: __jsl_clearance的值
        """
        # 转义字符
        js = second_js.replace('\\\\', '\\')

        # 切割
        js = 'cookie' + js.split('document.cookie')[1]
        js = js.split('GMT;Path=/;')[0] + "'"

        if re.findall("(var .{0,5}=)document\.createElement\('div'\);", js):
            js = self.replace_url(js)

        # 替换可能出现的window
        js = self.regex(js)

        s = """
            function cook() {
            %s
            return cookie
            }
            """
        new_js = s % js
        ctx = execjs.compile(new_js)
        # 切割获得的__jsl_clearance
        jsl = ctx.call('cook')
        jsl = jsl.split(';')[0]
        jsl_clearance = jsl.split('=')[1]
        return jsl_clearance

    def get_first_JSESSIONID(self, jsluid, jsl_clearance):
        """
        带cookies访问,测试拿到的是否正确
        :param jsluid:cookies中的参数
        :param jsl_clearance: cookies中的参数
        :return:
        """
        headers = self.headers.copy()
        headers['Cookie'] = f'__jsluid_h={jsluid}; __jsl_clearance={jsl_clearance};'
        response = requests.get(self.url, headers=headers)
        JSESSIONID = re.findall('JSESSIONID=(.*?);', response.headers['Set-Cookie'])[0]
        return JSESSIONID

    def get_JSESSIONID(self, jsluid, jsl_clearance, JSESSIONID):
        """
        每次请求都更换JSESSIONID
        :param jsluid:
        :param jsl_clearance:
        :param JSESSIONID:
        :return:
        """
        url = 'http://www.gsxt.gov.cn/SearchItemCaptcha?t=' + str(int(time.time()*1000))
        headers = self.headers.copy()
        headers['Cookie'] = f'__jsluid_h={jsluid}; __jsl_clearance={jsl_clearance};JSESSIONID={JSESSIONID}'
        response = requests.get(url, headers=headers)
        JSESSIONID = re.findall('JSESSIONID=(.*?);', response.headers['Set-Cookie'])[0]
        return JSESSIONID

    def test_cookies(self, jsluid, jsl_clearance, JSESSIONID):
        """
        带cookies访问,测试拿到的是否正确
        :param jsluid:cookies中的参数
        :param jsl_clearance: cookies中的参数
        :return:
        """
        headers = self.headers.copy()
        headers['Cookie'] = f'__jsluid_h={jsluid}; __jsl_clearance={jsl_clearance};JSESSIONID={JSESSIONID}'
        response = requests.get(self.test_url, headers=headers)
        print(response.text)
        return response.status_code

    def run(self):
        while True:
            first_js, jsluid = self.acquire_js()
            second_js = self.first_decryption(first_js)
            try:
                jsl_clearance = self.second_decryption(second_js)
            except:
                print(second_js)
                continue
            else:
                JSESSIONID = self.get_first_JSESSIONID(jsluid, jsl_clearance)
                JSESSIONID = self.get_JSESSIONID(jsluid, jsl_clearance, JSESSIONID)
                code = self.test_cookies(jsluid, jsl_clearance, JSESSIONID)
                if code == 200:
                    return jsluid, jsl_clearance, JSESSIONID
                else:
                    print(code)
                    print(second_js)
                    continue

    def run1(self):

        first_js, jsluid = self.acquire_js()
        second_js = self.first_decryption(first_js)
        jsl_clearance = self.second_decryption(second_js)
        print(jsluid, jsl_clearance)
        JSESSIONID = self.get_first_JSESSIONID(jsluid, jsl_clea0rance)
        print(JSESSIONID)
        JSESSIONID = self.get_JSESSIONID(jsluid, jsl_clearance, JSESSIONID)
        code = self.test_cookies(jsluid, jsl_clearance, JSESSIONID)
        print(code)


if __name__ == '__main__':
    url = "http://www.gsxt.gov.cn/index.html"
    test_url = "http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000"

    ck = Crack(url, test_url)
    jsluid, jsl_clearance, JSESSIONID = ck.run()
    print('__jsluid_h:', jsluid)
    print('__jsl_clearance:', jsl_clearance)
    print('JSESSIONID:', JSESSIONID)
