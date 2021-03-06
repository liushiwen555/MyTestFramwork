# -*- coding: utf-8 -*-
# @Time     : 2020/12/7 3:08 下午
# @Author   : LiuShiWen

"""
封装获取cookie方法
"""

import requests
from Common.getLog import logger
from Common.getConfig import Config


class Session:
    def __init__(self):
        self.config = Config()
        self.err_logger = logger("error")

    def get_session(self, env):
        """
        获取session
        :param env: 环境变量
        :return:
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        if env == "debug":
            login_url = 'http://' + self.config.loginHost_debug
            parm = self.config.loginInfo_debug

            session_debug = requests.session()
            response = session_debug.post(login_url, parm, headers=headers)
            print(response.cookies)
            logger().info('cookies: %s' % response.cookies.get_dict())
            return response.cookies.get_dict()

        elif env == "release":
            login_url = 'http://' + self.config.loginHost_release
            parm = self.config.loginInfo_release

            session_release = requests.session()
            response = session_release.post(login_url, parm, headers=headers)
            print(response.cookies)
            logger().info('cookies: %s' % response.cookies.get_dict())
            return response.cookies.get_dict()

        else:
            print("get cookies error")
            self.err_logger('get cookies error, please checkout!!!')


if __name__ == '__main__':
    ss = Session()
    ss.get_session('debug')
