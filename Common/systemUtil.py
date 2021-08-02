# -*- coding: utf-8 -*-
# @Time     : 2021/8/2 9:59 上午
# @Author   : LiuShiWen

import os

import os


def file_name_walk(file_name):
    project_path = os.getcwd()
    print(project_path)
    for root, dirs, files in os.walk(file_name):
        # print("root", root)  # 当前目录路径
        # print("dirs", dirs)  # 当前路径下所有子目录
        # print("files", files)  # 当前路径下所有非目录子文件
        for file in files:
            if not file.startswith("all") and file.endswith("pcap"):
                file_path = os.path.join(file_name, file)
                os.system("sudo tcpreplay -i enp7s0 -M2 -l 10 {}".format(file_path))

def search_dir(path):
    if not os.path.exists(path):
        print("路径不存在")
        return
    # 遍历第一层的文件夹或者文件
    file_list = os.listdir(path)  # ['dir1', 'dir1.py', 'dir2', 'dir2.py', 'dir3']
    # print(file_list)
    for file in file_list:
        # 获取 file 所对应的绝对路径
        file_path = os.path.join(path, file)
        # print(file_path)
        # 判断file_path是否是文件
        if os.path.isfile(file_path):
            print(f"文件：{file_path}")
            # if not file.startswith("all") and file.endswith("pcap"):
            #     print(file_path)
                # os.system("sudo tcpreplay -i enp7s0 -M2 -l 10 {}".format(file_path))
        # 否则是文件夹
        else:
            print(f"文件夹：{file}")
            # 递归
            search_dir(file_path)


if __name__ == '__main__':
    # file_name_walk("/Users/liushiwen/PycharmProjects/MyTestFramwoek/Common")
    path1 = r"/Users/liushiwen/PycharmProjects/MyTestFramwoek/OutPuts"
    search_dir(path1)