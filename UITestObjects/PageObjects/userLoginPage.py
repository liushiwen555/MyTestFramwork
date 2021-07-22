# -*- coding: utf-8 -*-
# @Time     : 2021/1/20 3:44 下午
# @Author   : LiuShiWen

from UITestObjects.BaseFactory.basepage import BasePage
from UITestObjects.Locators.userLoginLocator import UserLoginLocator
from Common.getCaptcha import get_captcha
import time


class UserLoginPage(BasePage):
    def __init__(self, browser_type='chrome'):
        BasePage.__init__(self, browser_type)
        self.locator = UserLoginLocator

    def goto_user_login_page(self):
        self.get('http://localhost:8080/jpress/user/login')

    def input_username(self, username):
        self.clear(*self.locator.input_user)
        self.send_keys(*self.locator.input_user, username)

    def input_pwd(self, pwd):
        self.clear(*self.locator.input_pwd)
        self.send_keys(*self.locator.input_pwd, pwd)

    def input_captcha(self):
        self.clear(*self.locator.input_captcha)
        captcha = self.get_captcha()
        self.send_keys(*self.locator.input_captcha, captcha)

    def click_login_button(self):
        self.click(*self.locator.button_login)

    def click_register_href(self):
        self.click(*self.locator.href_register)

    def get_captcha(self):
        return get_captcha(self.driver, *self.locator.captcha_img)

    def get_input_error_text(self, input_label):
        """
        获取input输入框错误提示
        :param input_label: 'username'，'pwd'，'captcha'
        :return:
        """
        try:
            if input_label == 'username':
                return self.get_text(*self.locator.username_error)
            elif input_label == 'pwd':
                return self.get_text(*self.locator.pwd_error)
            elif input_label == 'captcha':
                return self.get_text(*self.locator.captcha_error)
        except Exception:
            raise Exception("input_label 传参错误，请检查参数是否包含相关内容")


if __name__ == '__main__':
    login = UserLoginPage()
    login.goto_user_login_page()
    login.input_username('username')
    login.input_pwd('pwd')
    login.input_captcha()
    login.click_login_button()
    time.sleep(3)
    login.quit()