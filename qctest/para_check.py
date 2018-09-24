#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-9-16 22:49
# @Author  : lzzhang
# @Site    : 
# @File    : para_check.py
# @Software: PyCharm


class ParaChecker(object):
    def wrong_para(self, msg):
        raise Exception(msg)

    def check_integer_paras(self, valid_paras, int_paras):
        """ 检测整数类型参数
        :param valid_paras:
        :param int_paras:
        :return:
        """
        for para in int_paras:
            if para not in valid_paras:
                continue
            if not isinstance(valid_paras[para], int):
                self.wrong_para("parameter %s should be an integer." % para)
        return True

    def check_list_paras(self, valid_paras, list_paras):
        """
        检测列表类型参数
        :param valid_paras:
        :param list_paras:
        :return:
        """
        for para in list_paras:
            if para not in valid_paras:
                continue
            if not isinstance(valid_paras[para], list):
                self.wrong_para("parameter %s should be a list."%para)
        return True

    def check_required_paras(self, valid_paras, required_paras):
        """ 检测必填参数
        :param valid_paras:
        :param required_paras:
        :return:
        """
        for para in required_paras:
            if para not in valid_paras:
                self.wrong_para("parameter %s is required." % para)
        return True

    def check_paras(self, valid_paras, required_paras=None, integer_paras=None, list_paras=None):
        """
        检测有效参数
        :param valid_paras:
        :param required_paras:
        :param integer_paras:
        :param list_paras:
        :return:
        """
        if required_paras:
            self.check_required_paras(valid_paras, required_paras)
        if integer_paras:
            self.check_integer_paras(valid_paras, integer_paras)
        if list_paras:
            self.check_list_paras(valid_paras, list_paras)
        return True
