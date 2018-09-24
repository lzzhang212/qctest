#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-9-18 8:36
# @Author  : lzzhang
# @Site    : 
# @File    : unitest.py
# @Software: PyCharm


import unittest
from qctest.request_send import HTTPRequest
from qctest.qingcloud_api import describe_instances, run_instances, terminate_instances


class QingcloudTest(unittest.TestCase):
    def test_get_userinfo_run(self):
        rq = HTTPRequest()
        self.assertEqual(rq.userinfo['access_key_id'], 'QYACCESSKEYIDEXAMPLE')
        self.assertEqual(rq.userinfo['secret_access_key'], 'SECRETACCESSKEY')
        self.assertEqual(rq.userinfo['zone'], 'pek1')

    def test_paras2url_run(self):
        rq = HTTPRequest()
        paras = {"count":1,
                 "vxnets.1":"vxnet-0",
                 "zone":"pek1",
                 "instance_type":"small_b",
                 "signature_version":1,
                 "signature_method":"HmacSHA256",
                 "instance_name":"demo",
                 "image_id":"centos64x86a",
                 "login_mode":"passwd",
                 "login_passwd":"QingCloud20130712",
                 "version":1,
                 "access_key_id":"QYACCESSKEYIDEXAMPLE",
                 "action":"RunInstances",
                 "time_stamp":"2013-08-27T14:30:10Z"
                 }
        url = ('access_key_id=QYACCESSKEYIDEXAMPLE&action=RunInstances&count=1'
               '&image_id=centos64x86a&instance_name=demo&instance_type=small_b&login_mode=passwd'
               '&login_passwd=QingCloud20130712&signature_method=HmacSHA256&signature_version=1'
               '&time_stamp=2013-08-27T14%3A30%3A10Z&version=1&vxnets.1=vxnet-0&zone=pek1'
               )
        self.assertEqual(rq.paras_to_url(paras), url)

    def test_sign_run(self):
        rq = HTTPRequest()
        paras = {"count":1,
                 "vxnets.1":"vxnet-0",
                 "zone":"pek1",
                 "instance_type":"small_b",
                 "signature_version":1,
                 "signature_method":"HmacSHA256",
                 "instance_name":"demo",
                 "image_id":"centos64x86a",
                 "login_mode":"passwd",
                 "login_passwd":"QingCloud20130712",
                 "version":1,
                 "access_key_id":"QYACCESSKEYIDEXAMPLE",
                 "action":"RunInstances",
                 "time_stamp":"2013-08-27T14:30:10Z"
                }
        signature = rq.create_signature('GET', paras, '/iaas/')
        answer = '32bseYy39DOlatuewpeuW5vpmW51sD1A%2FJdGynqSpP8%3D'
        self.assertEqual(signature, answer)

    def test_desc_instance_run(self):
        ret_code = describe_instances()
        self.assertEqual(ret_code, 0)

    def test_run_instance_run(self):
        ret_code = run_instances(image_id='centos68x64a', login_mode='passwd', instance_type='c1m1', login_passwd='root212ZLZ')
        self.assertEqual(ret_code, 0)

    def test_ter_instance_run(self):
        ret_code = terminate_instances(instances='i-sjfrqqve')
        self.assertEqual(ret_code, 0)


if __name__ == '__main__':
    # unittest.main()
    t = QingcloudTest()
    t.test_get_userinfo_run()
    t.test_paras2url_run()
    t.test_sign_run()
    # t.test_run_instance_run()
    # t.test_desc_instance_run()
    # t.test_ter_instance_run()
