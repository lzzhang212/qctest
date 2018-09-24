#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-9-16 22:51
# @Author  : lzzhang
# @Site    : 
# @File    : request_send.py
# @Software: PyCharm


import os
import datetime
import requests
import base64
import hmac
from hashlib import sha256, sha1
from urllib.parse import quote, quote_plus

API_VERSION = 1
SIGNATURE_VERSION = 1
HMACSHA256 = 'HmacSHA256'
HMACSHA1 = 'HmacSHA1'


class HTTPRequest(object):
    user_file = 'user.txt'

    def __init__(self):
        self.userinfo = {}
        if not os.path.isfile(self.user_file):
            raise Exception("Please create file '{}'".format(self.user_file))
        # 从文件中获取用户相关的公共参数
        with open(self.user_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                key, value = line.split(':')
                self.userinfo[key] = value
        if 'zone' not in self.userinfo:
            raise Exception("Please enter the zone like zone:pek1.")
        if 'access_key_id' not in self.userinfo:
            raise Exception("Please enter the access_key_id like 'access_key_id:QYACCESSKEYIDEXAMPLE'")
        if 'secret_access_key' not in self.userinfo:
            raise  Exception("Please enter the secret_access_key like 'secret_access_key:SECRETACCESSKEY'")

    def paras_to_url(self, paras):
        """
        将参数字典转化为对应URL
        :param paras:
        :return:str
        """
        copy_paras = {}
        # 将list类型的参数转化为key.n:value的形式
        for key in paras.keys():
            if isinstance(paras[key], list):
                value = paras[key]
                for i in range(1, len(value) + 1):
                    copy_paras['%s.%d' % (key, i)] = value[i - 1]
            else:
                copy_paras[key] = paras[key]

        keys = sorted(copy_paras.keys())
        url_list = []
        for key in keys:
            val = str(copy_paras[key])
            key = key.encode()
            url_list.append(quote(key, safe='') + '=' + quote(val, safe='-_~'))
        return '&'.join(url_list)

    def create_signature(self, method, paras, uri):
        """ 生成签名
        """
        string_to_sign = '%s\n%s\n'%(method, uri)
        # 参数未指定加密方式，则默认按HmacSHA256加密
        if 'signature_method' not in paras:
            paras['signature_method'] = HMACSHA256
        paras['signature_version'] = SIGNATURE_VERSION

        # 对参数名称和参数值进行URL编码并构造URL请求
        url = self.paras_to_url(paras)
        string_to_sign += url
        if paras['signature_method'] == HMACSHA256:
            h = hmac.new(bytes(self.userinfo['secret_access_key'],'utf-8'),
                         bytes(string_to_sign, 'utf-8'),
                         digestmod=sha256).digest()
        elif paras['signature'] == HMACSHA1:
            h = hmac.new(bytes(self.userinfo['secret_access_key'], 'utf-8'),
                         bytes(string_to_sign, 'utf-8'),
                         digestmod=sha1).digest()
        sign = base64.b64encode(h).strip()
        signature = quote_plus(sign)
        return signature

    def send_request(self, action, paras, method='GET'):
        """构造请求
        """
        # 添加公共参数
        paras['action'] = action
        paras['zone'] = self.userinfo['zone']
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        paras['time_stamp'] = time_stamp
        paras['access_key_id'] = self.userinfo['access_key_id']
        paras['version'] = API_VERSION

        # 创建签名
        signature = self.create_signature(method, paras, '/iaas/')

        # 将参数转为对应URL
        url = self.paras_to_url(paras)
        url = 'https://api.qingcloud.com/iaas/?' + url + '&signature=' + signature

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }

        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        s.headers = headers

        if method == 'POST':
            pass
        else:
            resp = s.get(url=url, timeout=10, verify=False)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise Exception('HTTP response status:%d'% resp.status_code)