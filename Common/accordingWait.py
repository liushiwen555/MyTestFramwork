# -*- coding: utf-8 -*-
# @Time     : 2020/11/2 8:59 下午
# @Author   : LiuShiWen

import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Common.getLog import logger


class WaitUtil(object):
    """
    title_is                                    -判断title是否出现，返回bool类型
    title_contains                              -判断title是否包含某些字符，布尔
    presence_of_element_located                 -判断某个元素是否被加到dom树里，并不代表该元素一定可见，WebElement
    visibility_of_element_located               -判断某个元素是否被添加到了dom里并且可见，宽和高都大于0，WebElement
    visibility_of                               -判断元素是否可见，如果可见就返回这个元素，WebElement
    presence_of_all_elements_located            -判断是否至少有1个元素存在于dom树中，列表
    visibility_of_any_elements_located          -判断是否至少有一个元素在页面中可见，列表
    text_to_be_present_in_element               -判断指定的元素中是否包含了预期的字符串，布尔
    text_to_be_present_in_element_value         -判断指定元素的属性值中是否包含了预期的字符串，布尔
    frame_to_be_available_and_switch_to_it      -判断该frame是否是否可以switch进去，布尔
    invisibility_of_element_located             -判断某个元素是否存在于dom或不可见，布尔
    element_to_be_clickable                     -判断某个元素中是否可见并且是enable的，代表可点击，布尔
    staleness_of                                -等待某个元素从dom树中移除，布尔
    element_to_be_selected                      -判断某个元素是否被选中了，一般用在下拉列表，布尔
    element_selection_state_to_be               -判断某个元素的选中状态是否符合预期，布尔
    element_located_selection_state_to_be       -判断某个元素的选中状态是否符合预期，布尔
    alert_is_present                            -判断页面上是否存在alert，布尔
    """
    def __init__(self, driver, timeout=20):
        """
        :param driver: WebDriver实例
        :param timeout: 超时时间,默认20s
        """
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
        self._driver = driver
        self._wait = WebDriverWait(self._driver, timeout)
        self.logger = logger("error")

    def title_is(self, expect_title):
        """
        判断title是否出现，type is bool
        :param expect_title: 传入期待的title信息,type is string
        :return:
        """
        try:
            self._wait.until(EC.title_is(expect_title))
        except:
            self.logger.error(traceback.format_exc())

    def title_contains(self, expect_contain_text):
        """
        判断title是否包含某些字符
        :param expect_contain_text: 期待包含的字符，type is string
        :return:
        """
        try:
            self._wait.until(EC.title_contains(expect_contain_text))
        except:
            self.logger.error(traceback.format_exc())

    def presence_of_element_located(self, locationType, locatorExpression):
        """
        判断元素是否被加载到dom树里，并不代表元素一定可见
        :param locationType: 定位方法，type is string，小写字母
        :param locatorExpression: 定位器表达式
        :return:
        """
        try:
            if locationType.lower() in self.locationTypeDict:
                self._wait.until(
                    EC.presence_of_element_located((
                        self.locationTypeDict[locationType.lower()],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def visibility_of_element_located(self, locationType, locatorExpression):
        """
        判断某个元素是否被添加到了dom里并且可见，宽和高都大于0
        :param locationType: 定位方法，type is string，小写字母
        :param locatorExpression: 定位器表达式
        :return:
        """
        try:
            if locationType.lower() in self.locationTypeDict:
                self._wait.until(
                    EC.visibility_of_element_located((
                        self.locationTypeDict[locationType.lower()],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def visibility_of(self,locationType,locatorExpression):
        """
        判断元素是否可见，如果可见就返回这个元素
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.visibility_of(self._driver.element(
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def presence_of_all_elements_located(self,locationType,locatorExpression):
        """
        判断是否至少有一个元素存在于dom树中,如果定位到就反回列表
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.presence_of_all_elements_located((
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def visibility_of_any_elements_located(self,locationType,locatorExpression):
        """
        判断是否至少有一个元素在页面中可见，如果定位到就返回列表
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.visibility_of_any_elements_located((
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def text_to_be_present_in_element(self,locationType,locatorExpression,expect_str):
        """
        判断指定的元素之中是否包含了预期的字符串，返回布尔值
        :param locationType:
        :param locatorExpression:
        :param current_str: 元素中预期包含的字符串
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.text_to_be_present_in_element((
                        self.locationTypeDict[locationType],locatorExpression
                    ), expect_str)
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def text_to_be_present_in_element_value(self,locationType,locatorExpression,expect_str):
        """
        判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
        :param locationType:
        :param locatorExpression:
        :param expect_str: 元素属性值中预期包含的字符串
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.text_to_be_present_in_element_value((
                        self.locationTypeDict[locationType],locatorExpression
                    ), expect_str)
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def frame_to_be_available_and_switch_to_it(self,locationType,locatorExpression):
        """
        判断frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.frame_to_be_available_and_switch_to_it((
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def invisibility_of_element_located(self,locationType,locatorExpression):
        """
        判断某个元素是否存在于dom或不可见，如果可见返回False，不可见返回这个元素
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.invisibility_of_element_located((
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def element_to_be_clickable(self,locationType,locatorExpression):
        """
        判断某个元素是否可见并且是enable的，是代表可点击
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.element_to_be_clickable((
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def staleness_of(self,locationType,locatorExpression):
        """
        等待某个元素从dom树移除
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.staleness_of(self._driver.find_element(
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def element_to_be_selected(self,locationType,locatorExpression):
        """
        判断某个元素是否被选中，一般用在下拉列表
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.element_to_be_selected(self._driver.find_element(
                        self.locationTypeDict[locationType],locatorExpression
                    ))
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def element_selection_state_to_be(self,locationType,locatorExpression):
        """
        判断某个元素的选中状态是否符合预期
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.element_selection_state_to_be(self._driver.find_element(
                        self.locationTypeDict[locationType],locatorExpression
                    ),True)
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def element_located_selection_state_to_be(self,locationType,locatorExpression):
        """
        判断某个元素的选中状态是否符合预期
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.element_located_selection_state_to_be((
                        self.locationTypeDict[locationType],locatorExpression
                    ),True)
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())

    def alert_is_present(self, locationType, locatorExpression):
        """
        判断页面上是否存在alert，如果有就切换到alert并返回alert的内容
        :param locationType:
        :param locatorExpression:
        :return:
        """
        try:
            if locationType in self.locationTypeDict:
                self._wait.until(
                    EC.alert_is_present()
                )
            else:
                raise TypeError("定位方式异常，请检查定位方式是否正确")
        except:
            self.logger.error(traceback.format_exc())