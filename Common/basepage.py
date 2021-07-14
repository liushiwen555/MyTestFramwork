# -*- coding: utf-8 -*-
# @Time     : 2021/7/2 3:07 下午
# @Author   : LiuShiWen

from selenium import webdriver

def setHeadlessTrue():
    """chrome无头模式设置"""
    opts = webdriver.ChromeOptions()
    # opts.set_headless(headless=True)      #已弃用
    # opts.headless = True
    opts.add_argument('-headless')
    return opts


driver = webdriver.Chrome(chrome_options=setHeadlessTrue())
driver.get("http://www.baidu.com")
print(driver.title)