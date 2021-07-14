# -*- coding: utf-8 -*-
# @Time     : 2021/7/13 2:01 下午
# @Author   : LiuShiWen

import ast

def stringToDict(string_data):
    """
    字符串转成字典方法
    :param string_data: 数据的编写格式需要与字典一致
    :return:
    """
    dict_data = ast.literal_eval(string_data)
    return dict_data
