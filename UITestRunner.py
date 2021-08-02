# -*- coding: utf-8 -*-
# @Time     : 2021/1/2 3:11 下午
# @Author   : LiuShiWen

import smtplib
import pytest

from TestCases.testUICases.testUserRegister import TestRegisterCase

if __name__ == '__main__':
    test_register = TestRegisterCase()
    pytest.main('-sv', 'test_register')
