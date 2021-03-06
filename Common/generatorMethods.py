# -*- coding: utf-8 -*-
# @Time     : 2020/11/14 5:19 下午
# @Author   : LiuShiWen

import random
from faker import Factory


class FakerData(object):
    """一些生成器方法，生成随机数，手机号，以及连续数字等，以便使用这些数据进行测试"""
    def __init__(self):
        self.fake = Factory().create('zh_CN')

    @property
    def random_phone_number(self):
        """随机手机号"""
        return self.fake.phone_number()

    @property
    def random_name(self):
        """随机姓名"""
        return self.fake.name()

    @property
    def random_address(self):
        """随机地址"""
        return self.fake.address()

    @property
    def random_email(self):
        """随机email"""
        return self.fake.email()

    @property
    def random_ipv4(self):
        """随机IPV4地址"""
        return self.fake.ipv4()

    def random_str(self, min_chars=0, max_chars=8):
        """长度在最大值与最小值之间的随机字符串"""
        return self.fake.pystr(min_chars=min_chars, max_chars=max_chars)

    def factory_generate_ids(self,starting_id=1, increment=1):
        """ 产生一个id随机生成器,返回一个生成器函数，调用这个函数产生生成器，从starting_id开始，步长为increment。 """
        def generate_started_ids():
            val = starting_id
            local_increment = increment
            while True:
                yield val
                val += local_increment
        return generate_started_ids

    def factory_choice_generator(self, values):
        """ 产生一个随机选项生成器,返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
        def choice_generator():
            my_list = list(values)
            rand = random.Random()
            while True:
                yield random.choice(my_list)
        return choice_generator


if __name__ == '__main__':
    fake = FakerData()
    print(fake.random_phone_number)
    print(fake.random_name)
    print(fake.random_address)
    print(fake.random_email)
    print(fake.random_ipv4)
    print(fake.random_str(min_chars=6, max_chars=8))
    id_gen = fake.factory_generate_ids(starting_id=0, increment=2)()
    for i in range(5):
        print(next(id_gen))

    choices = ['John', 'Sam', 'Lily', 'Rose']
    choice_gen = fake.factory_choice_generator(choices)()
    for i in range(5):
        print(next(choice_gen))