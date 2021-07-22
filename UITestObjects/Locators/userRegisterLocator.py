# -*- coding: utf-8 -*-
# @Time     : 2021/1/20 3:20 下午
# @Author   : LiuShiWen

from selenium.webdriver.common.by import By


class UserRegisterLocator():
    """用户注册页面元素定位方式和定位表达式"""

    """用户名输入框"""
    input_username = (By.NAME, 'username')

    """邮箱输入框"""
    input_email = (By.NAME, 'email')

    """密码输入框"""
    input_password = (By.NAME, 'pwd')

    """确认密码输入框"""
    input_confirmPwd = (By.NAME, 'confirmPwd')

    """验证码输入框"""
    input_captcha = (By.ID, 'captcha')

    """验证码图片"""
    captcha_img = (By.ID, 'captcha-img')

    """注册按钮"""
    button_register = (By.XPATH, '/html/body/div/div/div[2]/div/form/div[6]/div/button')

    """登录页面链接，文本是这里"""
    href_login = (By.XPATH, '/html/body/div/div/div[2]/div/form/div[6]/div/p/a')


