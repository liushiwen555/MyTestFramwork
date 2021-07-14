# -*- coding: utf-8 -*-
# $Author   : LiuShiWen
# $Date     : 2021/7/2 2:59 下午

from configparser import ConfigParser
import os
import sys

project_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
if sys.platform.startswith("win32"):
    conf_path = os.path.join(project_path, 'Config/config.ini').replace('/', '\\')
    log_path = os.path.join(project_path, 'OutPuts/Logs').replace('/', '\\')
    report_path = os.path.join(project_path, 'OutPuts/Reports').replace('/', '\\')
    img_path = os.path.join(project_path, 'OutPuts/Images').replace('/', '\\')
    UITestData_path = os.path.join(project_path, 'Data/UITestData').replace('/', '\\')
    APITestData_path = os.path.join(project_path, 'Data/APITestData').replace('/', '\\')
else:
    conf_path = os.path.join(project_path, 'Config/.config.ini')
    log_path = os.path.join(project_path, 'OutPuts/Logs')
    report_path = os.path.join(project_path, 'OutPuts/Reports')
    img_path = os.path.join(project_path, 'OutPuts/Images')
    UITestData_path = os.path.join(project_path, 'Data/UITestData')
    APITestData_path = os.path.join(project_path, 'Data/APITestData')
if not os.path.exists(conf_path):
    raise FileNotFoundError("请检查配置文件路径是否存在")
if not os.path.exists(log_path):
    raise FileNotFoundError("请检查日志文件路径是否存在")
if not os.path.exists(report_path):
    raise FileNotFoundError("请检查报告路径是否存在")
if not os.path.exists(img_path):
    raise FileNotFoundError("请检查照片路径是否存在")
if not  os.path.exists(UITestData_path):
    raise FileNotFoundError("请检查UI测试数据路径是否存在")
if not  os.path.exists(APITestData_path):
    raise FileNotFoundError("请检查API测试数据路径是否存在")

class Config(object):
    def __init__(self, conf_path=conf_path, encode="utf-8"):
        if os.path.exists(conf_path):
            self.__cfg_file = conf_path
        else:
            # 此处做其他异常处理或创建配置文件操作
            raise Exception
        self.__config = ConfigParser()
        self.__config.read(self.__cfg_file, encoding=encode)

    # 获取配置文件的所有section
    def get_sections(self):
        return self.__config.sections()

    # 获取指定section的所有option
    def get_options(self, section_name):
        if self.__config.has_section(section_name):
            return self.__config.options(section_name)
        else:
            raise Exception

    # 获取指定section下option的value值
    def get_option_value(self, section_name, option_name):
        if self.__config.has_option(section_name, option_name):
            return self.__config.get(section_name, option_name)

    # 获取指定section下的option的键值对
    def get_all_items(self, section):
        if self.__config.has_section(section):
            return self.__config.items(section)

    # 打印配置文件所有的值
    def print_all_items(self):
        for section in self.get_sections():
            print("[" + section + "]")
            for K, V in self.__config.items(section):
                print(K + "=" + V)

    # 增加section
    def add_new_section(self, new_section):
        if not self.__config.has_section(new_section):
            self.__config.add_section(new_section)
            self.__update_cfg_file()

    # 增加指定section下option
    def add_option(self, section_name, option_key, option_value):
        if self.__config.has_section(section_name):
            self.__config.set(section_name, option_key, option_value)
            self.__update_cfg_file()

    # 删除指定section
    def del_section(self, section_name):
        if self.__config.has_section(section_name):
            self.__config.remove_section(section_name)
            self.__update_cfg_file()

    # 删除指定section下的option
    def del_option(self, section_name, option_name):
        if self.__config.has_option(section_name, option_name):
            self.__config.remove_option(section_name, option_name)
            self.__update_cfg_file()

    # 更新指定section下的option的值
    def update_option_value(self, section_name, option_key, option_value):
        if self.__config.has_option(section_name, option_key):
            self.add_option(section_name, option_key, option_value)

    # 私有方法:操作配置文件的增删改时，更新配置文件的数据
    def __update_cfg_file(self):
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
    print(getEmailOptionValues())


