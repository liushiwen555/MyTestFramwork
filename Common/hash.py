# -*- coding: utf-8 -*-
# @Time     : 2021/1/13 3:07 下午
# @Author   : LiuShiWen
import traceback
from hashlib import sha1
from hashlib import md5
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Cipher import DES
import binascii
from Common.getLog import logger


"""#Crypto 使用的是pycryptodemo库"""

def my_md5(msg):
    """
    md5 算法加密
    :param msg: 需加密的字符串
    :return: 加密后的字符
    """
    hl = md5()
    hl.update(msg.encode('utf-8'))
    return hl.hexdigest()

def my_sha1(msg):
    """
    sha1 算法加密
    :param msg: 需加密的字符串
    :return: 加密后的字符
    """
    sh = sha1()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()

def my_sha256(msg):
    """
    sha256 算法加密
    :param msg: 需加密的字符串
    :return: 加密后的字符
    """
    sh = SHA256.new()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()

def my_des(msg, key):
    """
    DES 算法加密
    :param msg: 需加密的字符串,长度必须为8的倍数，不足添加'='
    :param key: 8个字符
    :return: 加密后的字符
    """
    de = DES.new(key, DES.MODE_ECB)
    mss = msg + (8 - (len(msg) % 8)) * '='
    text = de.encrypt(mss.encode())
    return binascii.b2a_hex(text).decode()

def my_aes_encrypt(msg, key, vi):
    """
    AES 算法的加密
    :param msg: 需加密的字符串
    :param key: 必须为16，24，32位
    :param vi: 必须为16位
    :return: 加密后的字符
    """
    obj = AES.new(key, AES.MODE_CBC, vi)
    txt = obj.encrypt(msg.encode())
    return binascii.b2a_hex(txt).decode()

def my_aes_decrypt(msg, key, vi):
    """
    AES 算法的解密
    :param msg: 需解密的字符串
    :param key: 必须为16，24，32位
    :param vi: 必须为16位
    :return: 加密后的字符
    """
    msg = binascii.a2b_hex(msg)
    obj = AES.new(key, AES.MODE_CBC, vi)
    return obj.decrypt(msg).decode()

def sign(sign_dict, private_key=None, encrypt_way='MD5'):
    """
    签名函数,传入待签名的字典，返回签名后字符串, 1.字典排序;2.拼接，用&连接，最后拼接上私钥;3.MD5加密
    :param sign_dict:
    :param private_key:
    :param encrypt_way:
    :return:
    """
    dict_keys = sign_dict.keys()
    dict_keys.sort()
    string = ''
    for key in dict_keys:
        if sign_dict[key] is None:
            pass
        else:
            string += '{0}={1}&'.format(key, sign_dict[key])
    string = string[0:len(string) - 1]
    string = string.replace(' ', '')
    return encrypt(string, salt=private_key, encrypt_way=encrypt_way)


def encrypt(string, salt='', encrypt_way='MD5'):
    """ 加密函数,根据输入的string与加密盐，按照encrypt方式进行加密，并返回加密后的字符串 """
    string += salt
    if encrypt_way.upper() == 'MD5':
        hash_string = md5()
    elif encrypt_way.upper() == 'SHA1':
        hash_string = sha1()
    else:
        logger('error', '请输入正确的加密方式，目前仅支持 MD5 或 SHA1')
        logger('error', traceback.format_exc())
        return False
    hash_string.update(string.encode())
    return hash_string.hexdigest()


if __name__ == '__main__':
    print(encrypt('100000307111111'))
    print(my_md5('100000307111111'))
