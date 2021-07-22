# -*- coding: utf-8 -*-
# @Time     : 2021/1/21 10:51 上午
# @Author   : LiuShiWen
import traceback

import pytest
from UITestObjects.PageObjects.userLoginPage import UserLoginPage
from Common.getLog import logger


class TestLogin(object):
    def setup_method(self):
        self.login = UserLoginPage()
        self.login.goto_user_login_page()
        self.logger = logger("error")

    def test_login(self):
        self.login.input_username('username')
        self.login.input_pwd('pwd')
        self.login.input_captcha()
        self.login.click_login_button()
        try:
            alert_text = self.login.get_alert_text()
            print(alert_text)
            assert alert_text == "用户名不正确"
        except Exception:
            self.logger.error("未捕获到alert事件")
            self.logger.error(traceback.format_exc())
            raise Exception

    def teardown_method(self):
        self.login.quit()


if __name__ == '__main__':
    pytest.main('-sv', 'testUserLogin.py')