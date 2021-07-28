# -*- coding: utf-8 -*-
# @Time     : 2021/7/28 12:10 下午
# @Author   : LiuShiWen

import pytest
from UITestObjects.BaseFactory.basepage import BasePage
from UITestObjects.PageObjects.userRegisterPage import UserRegisterPage


@pytest.fixture(scope="class")
def user_register_page():
    register = UserRegisterPage()
    register.goto_user_register_page()
    yield register
    register.quit()




















