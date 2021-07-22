# -*- coding: utf-8 -*-
# @Time     : 2021/1/19 9:42 上午
# @Author   : LiuShiWen

import os
import traceback
from Common.getLog import logger
from selenium import webdriver
from time import time, localtime, strftime, sleep
from Common.getConfig import DRIVER_PATH, IMG_PATH
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Common.accordingWait import WaitUtil

"""
# 根据传入的参数选择浏览器的driver去打开对应的浏览器
# 可根据需要自行扩展
"""

CHROMEDRIVER_PATH: str = os.path.join(DRIVER_PATH, 'chromedriver')
IEDRIVER_PATH: str = os.path.join(DRIVER_PATH, 'IEDriverServer')
PHANTOMJSDRIVER_PATH: str = os.path.join(DRIVER_PATH, 'phantomjs')
FIREFOXDRIVER_PATH: str = os.path.join(DRIVER_PATH, 'firefoxdriver')

TYPES = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
    'ie': webdriver.Ie,
    'phantomjs': webdriver.PhantomJS
}
EXECUTABLE_PATH = {
    'firefox': FIREFOXDRIVER_PATH,
    'chrome': CHROMEDRIVER_PATH,
    'ie': IEDRIVER_PATH,
    'phantomjs': PHANTOMJSDRIVER_PATH
}
logger = logger("error")


class BasePage(object):
    def __init__(self, browser_type='chrome'):
        self.locationTypeDict = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        try:
            browser_type = browser_type.lower()
            driver = None
            if browser_type in TYPES:
                driver = TYPES[browser_type]
            self.driver = driver(
                executable_path=EXECUTABLE_PATH[browser_type],
                options=self.setHeadlessTrue(status=False)
            )
        except NameError:
            logger.error("Not found this browser,You can enter 'firefox', 'chrome', 'ie' or 'phantomjs'")
            logger.error(traceback.format_exc())

    @staticmethod
    def setHeadlessTrue(status=True):
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

    def get(self, url, implicitly_wait=30):
        """
        Usage:
        driver.get("https://www.baidu.com")
        :param url:
        :param implicitly_wait: 默认30s
        :return:
        """
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            self.driver.implicitly_wait(implicitly_wait)
        except Exception:
            logger.error("请检查url格式是否正确")
            logger.error(traceback.format_exc())

    def close(self):
        """
        Simulates the user clicking the "close" button in the titlebar of a popup window or tab.
        Usage:
        driver.close()
        :return:
        """
        self.driver.close()

    def quit(self):
        """
        Quit the driver and close all the windows.
        Usage:
        driver.quit()
        :return:
        """
        self.driver.quit()

    def find_element(self, location_type, locator_expression):
        """
        返还定位元素element对象
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        try:
            return self.driver.find_element(self.locationTypeDict[location_type.lower()], locator_expression)
        except Exception:
            logger.error("请检查定位方式和定位表达式格式是否正确")
            logger.error(traceback.format_exc())

    def element_wait(self, location_type, locator_expression):
        """
        Waiting for an element to display.
        Usage:
        driver.element_wait("id", "kw")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        wait = WaitUtil(self.driver)
        try:
            wait.presence_of_element_located(
                locationType=self.locationTypeDict[location_type.lower()],
                locatorExpression=locator_expression
            )
        except NameError:
            logger.error("the correct targeting elements,'id','name','class','link_text','xpath','css'；"
                   "Check that the locator_expression is properly formatted")
            logger.error(traceback.format_exc())

    def max_window(self):
        """
        Set browser window maximized.
        Usage:
        driver.max_window()
        :return:
        """
        self.driver.maximize_window()

    def set_window(self, wide, high):
        """
        Set browser window wide and high.
        Usage:
        driver.set_window(wide,high)
        :param wide: 宽
        :param high: 高
        :return:
        """
        try:
            self.driver.set_window_size(wide, high)
        except Exception:
            logger.error("检查wide和high数据格式是否正确")
            logger.error(traceback.format_exc())

    def click(self, location_type, locator_expression):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..
        Usage:
        driver.click("id", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele.click()

    def send_keys(self, location_type, locator_expression, text):
        """
        Operation input box 发送value
        Usage:
        driver.send_keys("id", "locator_expression", text)
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :param text:
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele.send_keys(text)

    def clear(self, location_type, locator_expression):
        """
        Clear the contents of the input box.
        Usage:
        driver.clear("id", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele.clear()

    def right_click(self, location_type, locator_expression):
        """
        Right click element.
        Usage:
        driver.right_click("id", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ActionChains(self.driver).context_click(ele).perform()

    def move_to_element(self, location_type, locator_expression):
        """
        Mouse over the element.
        Usage:
        driver.move_to_element("id",locator_expression)
        :param location_type: 定位方式，id,xpath,name,css......
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ActionChains(self.driver).move_to_element(ele).perform()

    def double_click(self, location_type, locator_expression):
        """
        Double click element.
        Usage:
        driver.double_click("id", "locator_expression")
        :param location_type: 定位方式，id,xpath,name,css......
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ActionChains(self.driver).double_click(ele).perform()

    def drag_and_drop(self, start_location_type, start_locator_expression,
                      target_location_type, target_locator_expression):
        """
        Drags an element a certain distance and then drops it.
        Usage:
        driver.drag_and_drop("start_location_type", "start_locator_expression",
                      "target_location_type", "target_locator_expression")
        :param start_location_type: 起始定位方式
        :param start_locator_expression: 起始定位表达式
        :param target_location_type: 目标元素定位方式
        :param target_locator_expression: 目标元素定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[start_location_type.lower()],
            locator_expression=start_locator_expression
        )
        start_element = self.find_element(
            location_type=self.locationTypeDict[start_location_type.lower()],
            locator_expression=start_locator_expression
        )
        self.element_wait(
            location_type=self.locationTypeDict[target_location_type.lower()],
            locator_expression=target_locator_expression
        )
        tarfind_element = self.find_element(
            location_type=self.locationTypeDict[target_location_type.lower()],
            locator_expression=target_locator_expression
        )
        ActionChains(self.driver).drag_and_drop(start_element, tarfind_element).perform()

    def submit(self, location_type, locator_expression):
        """
        Submit the specified form.
        Usage:
        driver.submit("location_type", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele.submit()

    def refresh_current_page(self):
        """
        Refresh the current page.
        :Usage:
            driver.refresh_current_page()
        :return:
        """
        self.driver.refresh()

    def back_browser(self):
        """
        Goes one step backward in the browser history.
        :Usage:
            driver.back_browser()
        :return:
        """
        self.driver.back()

    def forward_browser(self):
        """
        Goes one step forward in the browser history.
        :Usage:
            driver.forward_browser()
        :return:
        """
        self.driver.forward()

    def js(self, script):
        """
        Execute JavaScript scripts.
        :Usage:
            driver.js("window.scrollTo(200,1000);")
        :param script:
        :return:
        """
        self.driver.execute_script(script)

    def get_attribute(self, location_type, locator_expression, name):
        """
        Gets the value of an element attribute.
        获取页面元素对象对应属性的值
        Usage:
            driver.get_attribute("location_type", "locator_expression","class")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :param name: 属性名
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        return ele.get_attribute(name)

    def get_text(self, location_type, locator_expression):
        """
        Get element text information.
        Usage:
            driver.get_text("location_type", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        return ele.text

    def get_display(self, location_type, locator_expression):
        """
        Gets the element to display,The return result is true or false.
        Usage:
            driver.get_display("location_type", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return: true or false
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        return ele.is_displayed()

    def get_title(self):
        """
        Get window title.
        Usage:
            driver.get_title()
        :return: window title text
        """
        return self.driver.title

    def get_url(self):
        """
        Get the URL address of the current page.
        Usage:
            driver.get_url()
        :return: url
        """
        return self.driver.current_url

    def save_screenshot(self, filename='screen_shot'):
        """
        Saves a screenshot of the current window to a PNG image file. Returns
           False if there is any IOError, else returns True. Use full paths in
           your filename.
        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.
        :Usage:
            driver.save_screenshot('foo.png')
        :param filename: 截图文件名
        :return:
        """
        day = strftime('%Y%m%d', localtime(time()))
        screenshot_path = os.path.join(IMG_PATH, 'screenshot', 'screenshot_%s' % day)
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '/%s_%s.png' % (st, filename))
        return screenshot

    def get_screenshot(self, filename='screen_shot'):
        """
        Get the current window screenshot.
        Saves a screenshot of the current window to a PNG image file. Returns
           False if there is any IOError, else returns True. Use full paths in
           your filename.
        :Args:
         - filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.
        :Usage:
            driver.get_screenshot('foo.png')
        :param filename: 截图要保存的文件名
        :return:
        """
        day = strftime('%Y%m%d', localtime(time()))
        screenshot_path = os.path.join(IMG_PATH, 'screenshot', 'screenshot_%s' % day)
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
        filepath = screenshot_path + '/%s_%s.png' % (st, filename)
        self.driver.get_screenshot_as_file(filepath)

    def implicitly_wait(self, time_to_wait=10):
        """
        Implicitly wait.All elements on the page.
        :Usage:
            driver.implicitly_wait(10)
        :param time_to_wait:
        :return:
        """
        self.driver.implicitly_wait(time_to_wait)

    def get_alert_text(self):
        """
        Gets the text of the Alert.
        :return:
        """
        sleep(1)
        return self.driver.switch_to.alert.text

    def alert_send_keys(self, value):
        """
        Pass a value to the Alert input field
        :param value:
        :return:
        """
        sleep(1)
        self.driver.switch_to.alert.send_keys(value)

    def alert_accept(self):
        """
        Accept warning box.
        :Usage:
            driver.alert_accept()
        :return:
        """
        sleep(1)
        self.driver.switch_to.alert.accept()

    def alert_dismiss(self):
        """
        Dismisses the alert available.
        :Usage:
            driver.alert_dismiss()
        :return:
        """
        sleep(1)
        self.driver.switch_to.alert.dismiss()

    def switch_to_frame(self, location_type, locator_expression):
        """
        Switch to the specified frame.
        :Usage:
            driver.switch_to_frame("location_type", "locator_expression")
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        iframe_ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        self.driver.switch_to.frame(iframe_ele)

    def switch_to_parent_iframe(self):
        """
        Switches focus to the parent context. If the current context is the top
        level browsing context, the context remains unchanged.
        :Usage:
            driver.switch_to.parent_frame()
        :return:
        """
        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        """
        Switch focus to the default frame.
        :Usage:
            driver.switch_to.default_content()
        :return:
        """
        self.driver.switch_to.default_content()

    def switch_to_new_window(self, location_type, locator_expression):
        """
        Open the new window and switch the handle to the newly opened window.
        :Usage:
            driver.switch_to_new_window()
        :param location_type:
        :param locator_expression:
        :return:
        """
        original_windows = self.driver.current_window_handle
        ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        ele.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self.driver.switch_to.window(handle)

    def switch_to_window(self, handle_index):
        """
        Switches focus to the specified window.
        :Args:
         - window_name: The name or window handle of the window to switch to.
        :Usage:
            driver.switch_to.window('main')
        :param handle_num: 通过下标取，handles为列表，索引从0开始
        :return:
        """
        all_handles = self.driver.window_handles
        try:
            window_handle = all_handles[handle_index]
            self.driver.switch_to.window(window_handle)
        except IndexError:
            logger.error("请检查index数据是否符合要求")
            logger.error(traceback.format_exc())

    def wait_and_save_exception(self, location_type, locator_expression, filename='exception_img'):
        """
        判断预期元素是否出现，未出现保存当前截图
        :param location_type:
        :param locator_expression:
        :param filename:
        :return:
        """
        try:
            self.element_wait(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            return True
        except Exception as e:
            day = strftime('%Y%m%d', localtime(time()))
            screenshot_path = os.path.join(IMG_PATH, 'screenshot', 'exceptionScreenshot', 'screenshot_%s' % day)
            if not os.path.exists(screenshot_path):
                os.makedirs(screenshot_path)
            st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
            filepath = screenshot_path + '/%s_%s.png' % (st, filename)
            self.driver.save_screenshot(filepath)
            logger.error("元素在预期时间内未加载出来，请检查前置参数")
            return False

    def wait_and_exception(self, location_type, locator_expression):
        """
        判断元素是否出现
        :param location_type:
        :param locator_expression:
        :return:
        """
        try:
            self.element_wait(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            return True
        except Exception as e:
            logger.error("预期元素未出现，请检查前置参是否正确")
            return False

    def select_by_visible_text(self, location_type, locator_expression, text):
        """
        Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:
            <option value="foo">Bar</option>
        :Args:
        - text - The visible text to match against
        throws NoSuchElementException If there is no option with specisied text in SELECT
        根据select 页面可见文本text选择
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :param text: 页面可见文本
        :return:
        """
        try:
            self.element_wait(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            select_ele = self.find_element(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            Select(select_ele).select_by_visible_text(text)
        except Exception:
            logger.error("请检查参数是否正确，数据格式是否正确，检查页面可见文本text是否存在")
            logger.error(traceback.format_exc())

    def select_by_index(self, location_type, locator_expression, index):
        """
        Select the option at the given index. This is done by examing the "index" attribute of an
           element, and not merely by counting.
        :Args:
        - index - The option at this index will be selected
        throws NoSuchElementException If there is no option with specisied index in SELECT
        根据select index去选择
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :param index: select 索引，从0开始
        :return:
        """
        try:
            self.element_wait(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            select_ele = self.find_element(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            Select(select_ele).select_by_index(index)
        except Exception:
            logger.error("请检查参数是否正确，数据格式是否正确，检查index是超限")
            logger.error(traceback.format_exc())

    def select_by_value(self, location_type, locator_expression, value):
        """
        Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:
           <option value="foo">Bar</option>
        :Args:
        - value - The value to match against
        throws NoSuchElementException If there is no option with specisied value in SELECT
        根据select 属性value选择
        :param location_type: 定位方式
        :param locator_expression: 定位表达式
        :param value: select包含属性的值
        :return:
        """
        try:
            self.element_wait(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            select_ele = self.find_element(
                location_type=self.locationTypeDict[location_type.lower()],
                locator_expression=locator_expression
            )
            Select(select_ele).select_by_value(value)
        except Exception:
            logger.error("请检查参数是否正确，数据格式是否正确，检查value是否存在")
            logger.error(traceback.format_exc())

    def time_control_no_readonly(self, location_type, locator_expression, value):
        """
        时间控件无readonly属性情况的处理方式，先定位到时间控件，
        如果有默认值的话先用clear把框内时间清空，然后send_keys格式一样的时间
        :param location_type:
        :param locator_expression:
        :param value: 与原time格式一样的时间
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        time_control_ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        time_control_ele.clear()
        time_control_ele.send_keys(value)

    def time_control_readonly_by_id(self, location_type="id", locator_expression=None, value=None):
        """
        时间控件有readonly属性，元素包含id属性的处理方式
        在document树通过Id方式查找叫locator_expression的时间框，通过移除某个属性removeAttribute方法去移除readonly属性
        :param location_type: id
        :param locator_expression: id定位表达式
        :param value:
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        time_control_ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        js_script = f"document.getElementById('{locator_expression}').removeAttribute('readonly')"
        self.js(js_script)
        time_control_ele.send_keys(value)

    def time_control_readonly_by_name(self, location_type="name", locator_expression=None, value=None):
        """
        时间控件有readonly属性，元素包含name属性的处理方式
        在document树通过name方式查找叫locator_expression的时间框，通过移除某个属性removeAttribute方法去移除readonly属性
        ByName返回的是一个列表，列表里面是叫noticeEndTime的所有控件，所以要用下标去取控件
        :param location_type: name
        :param locator_expression: name表达式
        :param value:
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        time_control_ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        js_script = f"document.getElementsByName('{locator_expression}')[0].removeAttribute('readonly')"
        self.js(js_script)
        time_control_ele.send_keys(value)

    def time_control_readonly_by_tag_name(self, location_type="xpath", locator_expression=None,
                                          tag_name=None, value=None):
        """
        时间控件有readonly属性，用tag_name定位的处理方式
        在document树通过tag_name方式查找叫locator_expression的时间框，通过移除某个属性removeAttribute方法去移除readonly属性
        ByTagName找到的也是一组列表，需要用下标去取
        :param location_type: xpath
        :param locator_expression: xpath表达式
        :param tag_name: 时间控件标签名
        :param value:
        :return:
        """
        self.element_wait(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        time_control_ele = self.find_element(
            location_type=self.locationTypeDict[location_type.lower()],
            locator_expression=locator_expression
        )
        js_script = f"document.getElementsByTagName('{tag_name}')[0].removeAttribute('readonly')"
        self.js(js_script)
        time_control_ele.send_keys(value)

    def window_scroll_by_absolute_position(self, location_value):
        """
        var相当于定义了一个变量，这里是定义了一个叫q的变量,
        调了js里面的一个叫scrollTop的方法，这个方法可以滚动滚动条，这里滚动多少可以传参
        :param location_value: 具体的值，这里相对位置0开始计算
        :return:
        """
        js_script = f"var q=window.scrollTo(0, {location_value})"
        self.js(js_script)

    def window_scroll_to_top(self):
        """
        滚动到页面顶部
        :return:
        """
        js_script = "var q=document.documentElement.scrollTop=0"
        self.js(js_script)

    def window_scroll_to_bottom(self):
        """
        滚动到页面底部
        :return:
        """
        js_script = "var q=document.documentElement.scrollTop=10000"
        self.js(js_script)

    def window_scroll_to_half(self):
        """
        滚动到页面底部
        :return:
        """
        js_script = "var q=window.scrollTo(0,document.body.scrollHeight*0.5)"
        self.js(js_script)

    def window_scroll_by(self, offset):
        """
        相对当前位置进行偏移，可以正偏移也可以负偏移
        :param offset: 偏移量，可正可负
        :return:
        """
        js_script = f"var q=window.scrollBy(0, {offset})"
        self.js(js_script)


if __name__ == '__main__':
    driver = BasePage(browser_type='chrome')
    driver.get("http://www.baidu.com")
    driver.find_element("id","kw").send_keys("selenium")
    driver.find_element("id", "su").click()
    driver.element_wait("xpath", '//*[@id="2"]/h3/a')
    driver.quit()
