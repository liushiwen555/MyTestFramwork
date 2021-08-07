# -*- coding: utf-8 -*-
# @Time     : 2021/8/3 9:23 上午
# @Author   : LiuShiWen

from Common.operateExcel import OperateXlsx
from Common.getLog import logger
from Common.getConfig import Config
from Common.util import stringToDict
from Common.generatorMethods import FakerData


class UserLoginTestData(object):
    def __init__(self):
        self.logger = logger(level="error")
        self.faker = FakerData()

    test_login_data = (['test555', 'test@123'], ['test555', ''], ['', 'test@123'])


if __name__ == '__main__':
    data = "{'UserName' : 'test555', 'Email' : 'test@qq.com'," \
           "'Password' : 'test@123', 'Confirm_Password' : 'test@123'}"