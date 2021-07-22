# -*- coding: utf-8 -*-
# @Time     : 2020/11/14 5:54 下午
# @Author   : LiuShiWen

"""
添加用于测试后台接口的前端client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口等等。
"""

import socket
import json
import requests
import asyncio
from getLog import logger

# 所有支持的前后前交互方法
METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']
err_logger = logger("error")


class HTTPClient(object):
    """http请求的client。初始化时传入url、method等，可以添加headers和cookies，但没有auth、proxy。"""

    def __init__(self, url, method='GET', headers=None, cookies=None):
        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            logger('不支持的method:{0}，请检查传入参数！'.format(self.method))
        self.set_headers(headers)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, params=None, data=None, **kwargs):
        response = self.session.request(method=self.method, url=self.url, params=params, data=data, **kwargs)
        response.encoding = 'utf-8'
        logger().info('{0} {1}'.format(self.method, self.url))
        logger().info('请求成功: {0}\n{1}'.format(response, response.text))
        return response


class TCPClient(object):
    """用于测试TCP协议的socket请求，对于WebSocket，socket.io需要另外的封装"""

    def __init__(self, domain, port, timeout=30, max_receive=102400):
        self.domain = domain
        self.port = port
        self.connected = 0  # 连接后置为1
        self.max_receive = max_receive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)

    def connect(self):
        """连接指定IP、端口"""
        if not self.connected:
            try:
                self._sock.connect((self.domain, self.port))
            except socket.error as e:
                err_logger.error().exception(e)
            else:
                self.connected = 1
                logger().info('TCPClient connect to {0}:{1} success.'.format(self.domain, self.port))

    def send(self, data, dtype='str', suffix=''):
        """向服务器端发送send_string，并返回信息，若报错，则返回None"""
        if dtype == 'json':
            send_string = json.dumps(data) + suffix
        else:
            send_string = data + suffix
        self.connect()
        if self.connected:
            try:
                self._sock.send(send_string.encode())
                logger().info('TCPClient Send {0}'.format(send_string))
            except socket.error as e:
                err_logger.exception(e)

            try:
                rec = self._sock.recv(self.max_receive).decode()
                if suffix:
                    rec = rec[:-len(suffix)]
                logger().debug('TCPClient received {0}'.format(rec))
                return rec
            except socket.error as e:
                err_logger.error().exception(e)

    def close(self):
        """关闭连接"""
        if self.connected:
            self._sock.close()
            logger().info('TCPClient closed.')


# 异步并发客户端
class Asyncio_Client(object):

    def __init__(self):
        self.loop=asyncio.get_event_loop()
        self.tasks=[]

    # 将异步函数介入任务列表。后续参数直接传给异步函数
    def set_task(self,task_fun,num,*args):
        for i in range(num):
            self.tasks.append(task_fun(*args))

    # 运行，获取返回结果
    def run(self):
        back=[]
        try:
            f = asyncio.wait(self.tasks)   # 创建future
            self.loop.run_until_complete(f)  # 等待future完成
        finally:
            pass
            # self.loop.run_forever()
            # self.loop.close()  # 当轮训器关闭以后，所有没有执行完成的协成将全部关闭