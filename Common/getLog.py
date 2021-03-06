# -*- coding: utf-8 -*-
# @Time     : 2020/11/21 3:05 下午
# @Author   : LiuShiWen

import logging
import os.path
import traceback
from Common.getConfig import Config


class SetLog(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, level='info'):
        """
        :param level:
        """
        if level in ['debug', 'info', 'warning']:
            self.log_path = os.path.join(Config().get_option_value('log', 'log_path'), 'pro.log')
        elif level in ['error', 'critical']:
            self.log_path = os.path.join(Config().get_option_value('log', 'log_path'), 'pro_err.log')
        else:
            raise Exception("请检查日志级别是否设置正确")
        self.level = self.level_relations[level]
        '''创建日志器'''
        self.log = logging.getLogger()
        self.log.handlers = []
        '''日志器设置日志级别'''
        self.log.setLevel(self.level)

    def setFormatter(self):
        """
        设置格式器
        """
        formatter1 = logging.Formatter(fmt="%(asctime)s ==> %(filename)s ==> %(levelname)s ==> %(message)s")
        formatter2 = logging.Formatter(fmt="%(asctime)s : %(filename)s : %(levelname)s : %(message)s")
        return formatter1, formatter2

    def setStreamHandle(self):
        """创建控制台处理器,将控制台处理器添加进日志器,控制台处理器设置日志级别,设置日志打印格式"""
        stream_handle = logging.StreamHandler()
        self.log.addHandler(stream_handle)
        stream_handle.setLevel(self.level)
        stream_handle.setFormatter(self.setFormatter()[0])

    def setFileHandle(self):
        """
        创建文件处理器，将文件处理器添加进格式器，给文件处理器添加日志输出格式，给文件处理器设置日志输出级别
        :return:
        """
        filehandle = logging.FileHandler(filename=self.log_path,mode="a",encoding="utf-8")
        self.log.addHandler(filehandle)
        filehandle.setFormatter(self.setFormatter()[1])
        filehandle.setLevel(self.level)

    @property
    def get_logger(self):
        """
        返还日志器
        :param file:
        :return:
        """
        self.setStreamHandle()
        self.setFileHandle()
        return self.log


def logger(level='info'):
    """
    直接调用logger，里面日志器已被处理过
    :param level: 'debug','info','warning'，'error', 'critical'
    :return:
    """
    level = level.lower()
    get_logger = SetLog(level=level).get_logger
    return get_logger


if __name__ == '__main__':
    log = logger("error")

    def func(num1, num2):
        try:
            num_sum = num1 * num2
            print(num_sum)
        except Exception as e:
            # raise e
            log.error(traceback.format_exc())
            # logger.info("weishahuiliangci")
    func(1, 2)
    func("hello", "python")

