# -*- coding: utf-8 -*-
# $Author   : LiuShiWen
# $Date     : 2020/12/12 2:59 下午

from configparser import ConfigParser
import os
import sys

BASE_PATH = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

if sys.platform.startswith("win32"):
    CONF_PATH = os.path.join(BASE_PATH, 'Config', '.config.ini').replace('/', '\\')
    LOG_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Logs').replace('/', '\\')
    REPORT_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Reports').replace('/', '\\')
    IMG_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Images').replace('/', '\\')
    UIDATA_PATH = os.path.join(BASE_PATH, 'Data', 'UITestData').replace('/', '\\')
    APIDATA_PATH = os.path.join(BASE_PATH, 'Data', 'APITestData').replace('/', '\\')
    DRIVER_PATH = os.path.join(BASE_PATH, 'BrowserDrivers').replace('/', '\\')
else:
    CONF_PATH = os.path.join(BASE_PATH, 'Config', '.config.ini')
    LOG_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Logs')
    REPORT_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Reports')
    IMG_PATH = os.path.join(BASE_PATH, 'OutPuts', 'Images')
    UIDATA_PATH = os.path.join(BASE_PATH, 'Data', 'UITestData')
    APIDATA_PATH = os.path.join(BASE_PATH, 'Data', 'APITestData')
    DRIVER_PATH = os.path.join(BASE_PATH, 'BrowserDrivers')

if not os.path.exists(CONF_PATH):
    raise FileNotFoundError("请检查配置文件路径是否存在")
if not os.path.exists(LOG_PATH):
    raise FileNotFoundError("请检查日志文件路径是否存在")
if not os.path.exists(REPORT_PATH):
    raise FileNotFoundError("请检查报告路径是否存在")
if not os.path.exists(IMG_PATH):
    raise FileNotFoundError("请检查照片路径是否存在")
if not  os.path.exists(UIDATA_PATH):
    raise FileNotFoundError("请检查UI测试数据路径是否存在")
if not  os.path.exists(APIDATA_PATH):
    raise FileNotFoundError("请检查API测试数据路径是否存在")
if not os.path.exists(DRIVER_PATH):
    raise FileNotFoundError("请检查浏览器驱动目录是否存在")

class Config(object):
    def __init__(self, conf_path=CONF_PATH, encode="utf-8"):
        if os.path.exists(conf_path):
            self.__cfg_file = conf_path
        else:
            # 此处做其他异常处理或创建配置文件操作
            raise Exception
        self.__config = ConfigParser()
        self.__config.read(self.__cfg_file, encoding=encode)

    @property
    def get_sections(self):
        """获取配置文件的所有section"""
        return self.__config.sections()

    def get_options(self, section_name):
        """获取指定section的所有option"""
        if self.__config.has_section(section_name):
            return self.__config.options(section_name)
        else:
            raise Exception

    def get_option_value(self, section_name, option_name):
        """获取指定section下option的value值"""
        if self.__config.has_option(section_name, option_name):
            return self.__config.get(section_name, option_name)

    def get_all_items(self, section):
        """获取指定section下的option的键值对"""
        if self.__config.has_section(section):
            return self.__config.items(section)

    def print_all_items(self):
        """打印配置文件所有的值"""
        for section in self.get_sections:
            print("[" + section + "]")
            for K, V in self.__config.items(section):
                print(K + "=" + V)

    def add_new_section(self, new_section):
        """增加section"""
        if not self.__config.has_section(new_section):
            self.__config.add_section(new_section)
            self.__update_cfg_file()

    def add_option(self, section_name, option_key, option_value):
        """增加指定section下option"""
        if self.__config.has_section(section_name):
            self.__config.set(section_name, option_key, option_value)
            self.__update_cfg_file()

    def del_section(self, section_name):
        """删除指定section"""
        if self.__config.has_section(section_name):
            self.__config.remove_section(section_name)
            self.__update_cfg_file()

    def del_option(self, section_name, option_name):
        """删除指定section下的option"""
        if self.__config.has_option(section_name, option_name):
            self.__config.remove_option(section_name, option_name)
            self.__update_cfg_file()

    def update_option_value(self, section_name, option_key, option_value):
        """更新指定section下的option的值"""
        if self.__config.has_option(section_name, option_key):
            self.add_option(section_name, option_key, option_value)

    def __update_cfg_file(self):
        """私有方法:操作配置文件的增删改时，更新配置文件的数据"""
        with open(self.__cfg_file, "w") as f:
            self.__config.write(f)

def getEmailOptionValues():
    config = Config()
    email_data = []
    email_username = config.get_option_value('email','username')
    email_authorization_code = config.get_option_value('email','authorization_code')
    email_data.append(email_username)
    email_data.append(email_authorization_code)
    return email_data


if __name__ == '__main__':
    # print(getEmailOptionValues())
    print(Config().print_all_items())


