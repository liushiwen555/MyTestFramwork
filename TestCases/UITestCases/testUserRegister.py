# -*- coding: utf-8 -*-
# @Time     : 2021/7/22 4:59 下午
# @Author   : LiuShiWen

import traceback
import pytest
from UITestObjects.PageObjects.userRegisterPage import UserRegisterPage
from Common.getLog import logger
from UITestObjects.UITestDataFactory.dataTestRegisterFactory import UITestDataFactory


class TestRegisterCase(object):
    # data = ({'UserName': 'test555', 'Email': 'test@qq.com', 'Password': 'test@123', 'Confirm_Password': 'test@123'})
    # data = ({'user': 1, 'pwd': 2}, {'age': 3, 'email': 'tom@qq.com'})

    def setup_method(self):
        self.register = UserRegisterPage()
        self.register.goto_user_register_page()
        self.logger = logger("error")

    # @pytest.mark.parametrize('dict_data', data)
    def test_success_register(self):
        """测试注册功能是否有效"""
        # print(dict_data)
        self.register.input_username('username')
        self.register.input_email('test@qq.com')
        self.register.input_pwd(pwd='test@123')
        self.register.input_confirm_pwd(confirm_pwd='test@123')
        self.register.input_captcha()
        self.register.click_register_button()
        alert_text = self.register.get_alert_text()
        print(alert_text)
        assert alert_text == "注册成功，点击确定进行登录。"

        # except Exception:
        #     raise Exception("未捕获到alert事件")

    def test_input_blank(self):
        # print(dict_data)
        self.register.input_username('')
        self.register.input_email('test@163.com')
        self.register.input_pwd(pwd='test@123')
        self.register.input_confirm_pwd(confirm_pwd='test@123')
        self.register.input_captcha()
        self.register.click_register_button()
        username_blank_text = self.register.get_input_error_text('username')
        assert username_blank_text == "这是必填内容"

    def teardown_method(self):
        self.register.quit()


if __name__ == '__main__':
    pytest.main('-sv', 'testUserLogin.py')