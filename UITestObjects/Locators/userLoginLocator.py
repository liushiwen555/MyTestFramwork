# -*- coding: utf-8 -*-
# @Time     : 2021/1/20 3:39 下午
# @Author   : LiuShiWen

from selenium.webdriver.common.by import By


class UserLoginLocator:
    """用户登录页面元素定位方式和定位表达式"""

    """用户名输入框"""
    input_user = (By.NAME, 'user')

    """密码输入框"""
    input_pwd = (By.NAME, 'pwd')

    """验证码输入框"""
    input_captcha = (By.ID, 'captcha')

    """验证码图片"""
    captcha_img = (By.ID, 'captcha-img')
    # captcha_img = (By.XPATH, '//*[@id="captcha-img"]')

    """登录按钮"""
    button_login = (By.XPATH, '/html/body/div/div/div[2]/div/form/div[4]/div/button')

    """注册页面链接"""
    href_register = (By.XPATH, '/html/body/div/div/div[2]/div/form/div[4]/div/p/a')