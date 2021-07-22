# -*- coding: utf-8 -*-
# @Time     : 2020/12/18 3:07 下午
# @Author   : LiuShiWen

import yaml
import os


class YamlReader:
    """读取配置文件yaml文件成配置内容"""
    def __init__(self, yamlfilepath):
        if os.path.exists(yamlfilepath):
            self.yamlfilepath = yamlfilepath
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        """如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据"""
        if not self._data:
            with open(self.yamlfilepath, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data