# -*- coding: utf-8 -*-
# @Time     : 2021/1/21 10:51 上午
# @Author   : LiuShiWen

import traceback
import pytest
import allure
from UITestObjects.PageObjects.userLoginPage import UserLoginPage
from Common.getLog import logger
from UITestObjects.UITestDataFactory.userLoginTestDataFactory import UserLoginTestData


class TestLoginCase(object):

    # test_login_data = UserLoginTestData().test_login_data
    test_login_data = (["test555", "test@123"], ["test556", "test@123"])

    @allure.title("必填限制测试")
    @allure.description("注册模块各输入项必填限制检查")
    @allure.link("https://192.168.3.189", name="项目地址")
    @allure.issue("https://ones.ai/project/#/team/WKcESQu7/project/4QQzma4BQ68apgNB/"
                  "component/dj3yOhrd/view/L9GGVMSE/task/3cs3j83EHgnrqPNB/0?isHideDialog=1",
                  name="ones bug链接")
    @allure.testcase("https://ones.ai/project/#/testcase/team/WKcESQu7/plan/PBa7CDEg/library",
                     name="ones case链接")
    @pytest.mark.parametrize("username, password", test_login_data)
    def test_login(self, username, password):
        body = "期望值：\n username: test123 \n password: test@123" + "\n" + \
               f"实际值: \n username: {username} \n password: {password}"
        # allure.attach(body, "校验", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f'<head></head><body> {body} </body>', "校验", allure.attachment_type.HTML)



if __name__ == '__main__':
    pytest.main('-sv', 'testUserLogin.py')