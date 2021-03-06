# -*- coding: utf-8 -*-
# @Time     : 2021/7/28 12:10 下午
# @Author   : LiuShiWen
import allure
import pytest
from Common.getLog import logger
from UITestObjects.BaseFactory.basepage import BasePage
from UITestObjects.PageObjects.userRegisterPage import UserRegisterPage

logger = logger()


@pytest.fixture(scope="function")
def user_register_page():
    register = UserRegisterPage()
    register.goto_user_register_page()
    logger.info("进入注册页面")
    yield register
    img = register.save_screenshot()
    allure.attach.file(source=img, name="截图", attachment_type=allure.attachment_type.PNG)
    register.quit()
    logger.info("退出浏览器")























