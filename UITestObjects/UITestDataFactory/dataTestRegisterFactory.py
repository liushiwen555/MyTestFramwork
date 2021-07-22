# -*- coding: utf-8 -*-
# @Time     : 2021/7/22 11:32 上午
# @Author   : LiuShiWen

from Common.operateExcel import OperateXlsx
from Common.getLog import logger
from Common.getConfig import Config
from Common.util import stringToDict
from Common.generatorMethods import FakerData


class UITestDataFactory():
    def __init__(self):
        self.logger = logger(level="error")
        self.faker = FakerData()

    def data_test_success_register(self):
        username = self.faker.random_str(min_chars=6, max_chars=8)
        email = self.faker.random_email
        pwd = self.faker.random_str(8, 16)
        confirm_pwd = pwd
        data_test = (username, email, pwd, confirm_pwd)
        return data_test



if __name__ == '__main__':
    data = "{'UserName' : 'test555', 'Email' : 'test@qq.com', " \
           "'Password' : 'test@123', 'Confirm_Password' : 'test@123'}"
    print(UITestDataFactory().data_test_success_register())