# -*- coding: utf-8 -*-
# @Time     : 2021/1/20 3:44 下午
# @Author   : LiuShiWen


from UITestObjects.BaseFactory.basepage import BasePage
from UITestObjects.Locators.userRegisterLocator import UserRegisterLocator
from Common.getCaptcha import get_captcha
import time


class UserRegisterPage(BasePage):
    def __init__(self, browser_type='chrome'):
        BasePage.__init__(self, browser_type)
        self.locator = UserRegisterLocator

    def goto_user_register_page(self):
        self.get('http://localhost:8080/jpress/user/register')

    def input_username(self, username):
        self.clear(*self.locator.input_username)
        self.send_keys(*self.locator.input_username, username)

    def input_email(self, email):
        self.clear(*self.locator.input_email)
        self.send_keys(*self.locator.input_email, email)

    def input_pwd(self, pwd):
        self.clear(*self.locator.input_password)
        self.send_keys(*self.locator.input_password, pwd)

    def input_confirm_pwd(self, confirm_pwd):
        self.clear(*self.locator.input_confirmPwd)
        self.send_keys(*self.locator.input_confirmPwd, confirm_pwd)

    def input_captcha(self):
        self.clear(*self.locator.input_captcha)
        captcha = self.get_captcha()
        self.send_keys(*self.locator.input_captcha, captcha)

    def click_register_button(self):
        self.click(*self.locator.button_register)

    def click_login_href(self):
        self.click(*self.locator.href_login)

    def get_captcha(self):
        return get_captcha(self.driver, *self.locator.captcha_img)

    def get_input_error_text(self, input_label):
        """
        获取input输入框错误提示
        :param input_label: 'username'，'email'，'pwd'，'confirm_pwd'，'captcha'
        :return:
        """
        try:
            if input_label == 'username':
                return self.get_text(*self.locator.username_error)
            elif input_label == 'email':
                return self.get_text(*self.locator.email_error)
            elif input_label == 'pwd':
                return self.get_text(*self.locator.pwd_error)
            elif input_label == 'confirm_pwd':
                return self.get_text(*self.locator.confirmPwd_error)
            elif input_label == 'captcha':
                return self.get_text(*self.locator.captcha_error)
        except Exception:
            raise Exception("input_label 传参错误，请检查参数是否包含相关内容")



if __name__ == '__main__':
    register = UserRegisterPage()
    register.goto_user_register_page()
    register.input_username("username")
    register.input_email("test123@qq.com")
    register.input_pwd("test@123")
    register.input_confirm_pwd("test123")
    register.input_captcha()
    register.click_register_button()
    time.sleep(5)
    register.quit()
