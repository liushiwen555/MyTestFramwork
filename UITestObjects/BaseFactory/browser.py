# -*- coding: utf-8 -*-
# @Time     : 2021/7/15 2:13 下午
# @Author   : LiuShiWen

import os
import traceback
from Common.getLog import logger
from selenium import webdriver
from time import time,localtime,strftime,sleep
from Common.getConfig import DRIVER_PATH, IMG_PATH


"""
# 根据传入的参数选择浏览器的driver去打开对应的浏览器
# 可根据需要自行扩展
"""

CHROMEDRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver')
IEDRIVER_PATH = os.path.join(DRIVER_PATH, 'IEDriverServer')
PHANTOMJSDRIVER_PATH = os.path.join(DRIVER_PATH, 'phantomjs')
FIREFOXDRIVER_PATH = os.path.join(DRIVER_PATH, 'firefoxdriver')

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie, 'phantomjs': webdriver.PhantomJS}
EXECUTABLE_PATH = {'firefox': FIREFOXDRIVER_PATH, 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH, 'phantomjs': PHANTOMJSDRIVER_PATH}

class Browser(object):
    def __init__(self, browser_type='chrome'):
        self.logger = logger("error")
        self._type = browser_type.lower()
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            self.logger.error('仅支持%s!' % ', '.join(TYPES.keys()))
        self.driver = None

    def setHeadlessTrue(self, status=True):
        """
        chrome无头模式设置
        :param status: True or False
        :return:
        """
        opts = webdriver.ChromeOptions()
        # opts.set_headless(headless=True)
        opts.headless = status
        # opts.add_argument('-headless')
        return opts

    def get(self, url, maximize_window=True, implicitly_wait=30):
        self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type],options=self.setHeadlessTrue(status=False))
        try:
            self.driver.get(url)
            if maximize_window:
                self.driver.maximize_window()
            self.driver.implicitly_wait(implicitly_wait)
            return self
        except:
            self.logger.error("请检查url格式是否正确")
            self.logger.error(traceback.format_exc())

    def save_screen_shot(self, name='screen_shot'):
        day = strftime('%Y%m%d', localtime(time()))
        screenshot_path = os.path.join(IMG_PATH, 'screenshot', 'screenshot_%s' % day)
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        # tm = time.strftime('%H%M%S', time.localtime(time.time()))
        st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '/%s_%s.png' % (name, st))
        return screenshot

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

class BrowserBAK(object):
    def __init__(self,driver):
        self.logger = logger("error")
        pass




if __name__ == '__main__':
    b = Browser().get("http://www.baidu.com")
    b.save_screen_shot('test_baidu')
    b.quit()