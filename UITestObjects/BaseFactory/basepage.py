# -*- coding: utf-8 -*-
# @Time     : 2021/7/2 3:07 下午
# @Author   : LiuShiWen


import time
from Common.getLog import logger
from browser import Browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class BasePage(Browser):
    """ 浏览器页面类，主要进行浏览器页面的控制，一些操作方法的封装 """
    def __init__(self, page=None, browser_type='chrome'):
        if page:
            self.driver = page.driver
        else:
            super(BasePage, self).__init__(browser_type=browser_type)

    @property
    def current_window(self):
        """ 获取当前窗口句柄 """
        return self.driver.current_window_handle

    @property
    def title(self):
        """ 获取标题 """
        return self.driver.title

    @property
    def current_url(self):
        """ 获取当前网址 """
        return self.driver.current_url

    def get_driver(self):
        """ 获取浏览器驱动 """
        return self.driver

    def wait(self, seconds=3):
        """ 睡眠一段时间 """
        time.sleep(seconds)

    def execute(self, js, *args):
        """ 执行js脚本 """
        self.driver.execute_script(js, *args)

    def move_to(self, element):
        """ 移动到指定元素 """
        ActionChains(self.driver).move_to_element(element).perform()

    def find_element(self, *args):
        """ 寻找指定元素 """
        return self.driver.find_element(*args)

    def find_elements(self, *args):
        """ 寻找指定的一批元素 """
        return self.driver.find_elements(*args)

    def switch_to_window(self, partial_url='', partial_title=''):
        """切换窗口
            如果窗口数<3,不需要传入参数，切换到当前窗口外的窗口；
            如果窗口数>=3，则需要传入参数来确定要跳转到哪个窗口
        """
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            logger.warning('只有1个window!')
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.driver.current_url or partial_title in self.driver.title:
                    break
        logger.debug(self.driver.current_url, self.driver.title)

    def switch_to_frame(self, param):
        """ 切换frame页面 """
        self.driver.switch_to.frame(param)

    def switch_to_alert(self):
        """ 切换alter """
        return self.driver.switch_to.alert



if __name__ == '__main__':

    # Browser().browser(chrome_options=BasePage().setHeadlessTrue)
    Browser().get("http://www.baidu.com")
    # driver = webdriver.Chrome(chrome_options=BasePage().setHeadlessTrue)
    # driver.get("http://www.baidu.com")
    print(BasePage().title)