# -*- coding: utf-8 -*-
# @Time     : 2020/12/6 9:50 上午
# @Author   : LiuShiWen

import random
import string
import datetime
import time

"""
    python中时间日期格式化符号：
    ------------------------------------
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）
    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为星期的开始
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称  # 乱码
    %% %号本身

    # datetime.timedelta 代表两个时间之间的时间差
    # time.strftime(fmt[,tupletime]) 接收以时间元组，并返回以可读字符串表示的当地时间，格式由fmt决定
    # time.strptime(str,fmt='%a %b %d %H:%M:%S %Y') 根据fmt的格式把一个时间字符串解析为时间元组
    # time.mktime(tupletime) 接受时间元组并返回时间戳（1970纪元后经过的浮点秒数）
"""

def get_time(time_type, layout, unit="0,0,0,0,0"):
    """
    获取时间
    :param time_type: 现在的时间now， 其他时间else_time
    :param layout: 10timestamp，13timestamp, else  时间类型
    :param unit: 时间单位：[seconds, minutes, hours, days, weeks] 秒，分，时，天，周，所有参数都是可选的，并且默认都是0
    :return:
    """
    ti = datetime.datetime.now()
    if time_type != "now":
        resolution = unit.split(",")
        try:
            ti = ti + datetime.timedelta(seconds=int(resolution[0]), minutes=int(resolution[1]),
                                         hours=int(resolution[2]), days=int(resolution[3]), weeks=int(resolution[4]))
        except ValueError:
            raise Exception("获取时间错误，时间单位%s" % unit)
    if layout == "10timestamp":
        ti = ti.strftime('%Y-%m-%d %H:%M:%S')
        ti = int(time.mktime(time.strptime(ti, "%Y-%m-%d %H:%M:%S")))
        return ti
    elif layout == "13timestamp":
        ti = ti.strftime('%Y-%m-%d %H:%M:%S')
        ti = int(time.mktime(time.strptime(ti, '%Y-%m-%d %H:%M:%S')))
        # round()是四舍五入
        ti = int(round(ti * 1000))
        return ti
    else:
        ti = ti.strftime(layout)
        return ti

def random_string(lenth=8):
    """
    随机字符串生成方法，默认生成8位字符串,字母数字组合
    :param lenth: int类型，默认8位
    :return:
    """
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits,lenth))
    return rand_str

def random_int(scope):
    """
    获取随机整型数据
    :param scope: type is string,数据范围,example: "100,200"
    :return: 传入范围内的随机整数
    """
    try:
        start_num, end_num = scope.split(",")
        start_num = int(start_num)
        end_num = int(end_num)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数有误！\n %s" % str(scope))
    if start_num <= end_num:
        num = random.randint(start_num, end_num)
    else:
        num = random.randint(end_num, start_num)
    return num

def choice_data(data):
    """
    获取随机整型数据
    :param data: type is string，example: "100,22,234"
    :return:
    """
    _list = data.split(",")
    num = random.choice(_list)
    return num



if __name__ == '__main__':
    print(get_time("now", "13timestamp", "12,12,12,12,12"))
    print(get_time("now", "%Y-%m-%d %H:%M:%S"))
    print(get_time("else", '%Y-%m-%d %H:%M:%S', '0,0,0,5,0'))
    print(random_string(62))
    print(random_int("100,200"))
    print(choice_data("200,234,212"))

