# -*- coding: utf-8 -*-
# @Time     : 2021/7/20 3:44 下午
# @Author   : LiuShiWen

from UITestObjects.BaseFactory.basepage import BasePage
from UITestObjects.Locators.userLoginLocator import UserLoginLocator


class UserLoginPage(BasePage):
    def __init__(self, browser_type='chrome'):
        BasePage.__init__(self, browser_type)
        self.driver = BasePage(browser_type)

    def goto_user_login_page(self):
        self.driver.get('http://localhost:8080/jpress/user/login')

    def input_username(self, username):
        pass

    def input_pwd(self, pwd):
        pass

    def input_captcha(self, captcha):
        pass

    def click_login_button(self):
        pass

    def click_register_href(self):
        pass


if __name__ == '__main__':
    login = UserLoginPage()
    login.goto_user_login_page()