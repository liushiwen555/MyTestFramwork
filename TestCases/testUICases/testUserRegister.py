# -*- coding: utf-8 -*-
# @Time     : 2021/7/22 4:59 下午
# @Author   : LiuShiWen

import time
import traceback
import allure
import pytest
from Common.getLog import logger
from UITestObjects.PageObjects.userRegisterPage import UserRegisterPage
from Common.getLog import logger
from UITestObjects.Locators.userRegisterLocator import UserRegisterLocator
from UITestObjects.UITestDataFactory.userRegisterTestDataFactory import UserRegisterTestData

logger = logger()


class TestRegisterCase(object):
    test_data = UserRegisterTestData()
    test_input_blank_data = test_data.test_input_blank_data
    success_register_data = test_data.success_register_data()

    @allure.title("必填限制测试，测试数据：{dict_data}")
    @allure.description("注册模块各输入项必填限制检查")
    @allure.link("https://192.168.3.189", name="项目地址")
    @allure.issue("https://ones.ai/project/#/team/WKcESQu7/project/4QQzma4BQ68apgNB/"
                  "component/dj3yOhrd/view/L9GGVMSE/task/3cs3j83EHgnrqPNB/0?isHideDialog=1",
                  name="ones bug链接")
    @allure.testcase("https://ones.ai/project/#/testcase/team/WKcESQu7/plan/PBa7CDEg/library",
                     name="ones case链接")
    @pytest.mark.parametrize('dict_data', test_input_blank_data)
    def test_input_blank(self, dict_data, user_register_page):
        register = user_register_page
        register.input_username(dict_data['UserName'])
        register.input_email(dict_data['Email'])
        register.input_pwd(dict_data['Password'])
        register.input_confirm_pwd(dict_data['Confirm_Password'])
        register.input_captcha()
        if len(dict_data['UserName']) == 0:
            register.click_register_button()
            username_blank_text = register.get_input_error_text('username')
            pytest.assume(username_blank_text == "这是必填内容")
        if len(dict_data['Email']) == 0:
            register.click_register_button()
            email_blank_text = register.get_input_error_text('email')
            pytest.assume(email_blank_text == "这是必填内容")
        if len(dict_data['Password']) == 0:
            register.click_register_button()
            password_blank_text = register.get_input_error_text('pwd')
            pytest.assume(password_blank_text == "这是必填内容")
        if len(dict_data['Confirm_Password']) == 0:
            register.click_register_button()
            confirm_pwd_blank_text = register.get_input_error_text('confirm_pwd')
            pytest.assume(confirm_pwd_blank_text == "这是必填内容")
        if len(dict_data['UserName']) != 0 and len(dict_data['Email']) != 0\
                and len(dict_data['Password']) != 0 and len(dict_data['Confirm_Password']) != 0:
            register.clear(*UserRegisterLocator.input_captcha)
            register.click_register_button()
            captcha_blank_text = register.get_input_error_text('captcha')
            pytest.assume(captcha_blank_text == "这是必填内容")

    @allure.title("测试注册功能，测试数据:{username}, {email}, {pwd}, {confirm_pwd}")
    @allure.description("测试注册功能是否有效")
    @allure.link("https://192.168.3.189", name="项目地址")
    @allure.issue("https://ones.ai/project/#/team/WKcESQu7/project/4QQzma4BQ68apgNB/"
                  "component/dj3yOhrd/view/L9GGVMSE/task/3cs3j83EHgnrqPNB/0?isHideDialog=1",
                  name="ones bug链接")
    @allure.testcase("https://ones.ai/project/#/testcase/team/WKcESQu7/plan/PBa7CDEg/library",
                     name="ones case链接")
    @pytest.mark.parametrize('username, email, pwd, confirm_pwd', success_register_data)
    def test_success_register(self, username, email, pwd, confirm_pwd, user_register_page):
        register = user_register_page
        register.input_username(username)
        register.input_email(email)
        register.input_pwd(pwd)
        register.input_confirm_pwd(confirm_pwd)
        register.input_captcha()
        register.click_register_button()
        success_register_text = register.get_alert_text()
        register.alert_accept()
        assert success_register_text == "注册成功，点击确定进行登录"


if __name__ == '__main__':
    pytest.main('-sv', 'testUserLogin.py')