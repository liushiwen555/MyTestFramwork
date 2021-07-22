# -*- coding: utf-8 -*-
# @Time     : 2020/11/13 2:01 下午
# @Author   : LiuShiWen

import ast
import json
import base64
import jmespath
from Common.client import HTTPClient


def imgToBase64(img):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
        return b64

def base64ToImg(b64_value):
    img = base64.b64decode(b64_value)
    with open("pic.jpg", "wb") as fh:
        fh.write(img)

def stringToDict(string_data):
    """
    字符串转成字典方法
    :param string_data: 数据的编写格式需要与字典一致
    :return:
    """
    dict_data = ast.literal_eval(string_data)
    return dict_data

class JMESPathExtractor(object):
    """
    抽取器，从响应结果中抽取部分数据，这里实现的是json返回数据的抽取，可以自己添加XML格式、普通字符串格式、Header的抽取器
    完成了对JSON格式的抽取器，如果返回结果是JSON串，我们可以通过这个抽取器找到我们想要的数据，再进行下一步的操作，或者用来做断言。
    用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))




if __name__ == '__main__':

    res = HTTPClient(url='http://wthrcdn.etouch.cn/weather_mini?citykey=101010100').send()
    print(res.text)
    # {"data": {
    #     "yesterday": {"date": "17日星期四", "high": "高温 31℃", "fx": "东南风", "low": "低温 22℃", "fl": "<![CDATA[<3级]]>",
    #                   "type": "多云"},
    #     "city": "北京",
    #     "aqi": "91",
    #     "forecast": [
    #         {"date": "18日星期五", "high": "高温 28℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 22℃", "fengxiang": "东北风",
    #          "type": "多云"},
    #         {"date": "19日星期六", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 22℃", "fengxiang": "东风",
    #          "type": "雷阵雨"},
    #         {"date": "20日星期天", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 23℃", "fengxiang": "东南风",
    #          "type": "阴"},
    #         {"date": "21日星期一", "high": "高温 30℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 24℃", "fengxiang": "西南风",
    #          "type": "晴"},
    #         {"date": "22日星期二", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 24℃", "fengxiang": "北风",
    #          "type": "雷阵雨"}
    #     ],
    #     "ganmao": "各项气象条件适宜，无明显降温过程，发生感冒机率较低。", "wendu": "25"
    #  },
    # "status": 1000,
    # "desc": "OK"}

    j = JMESPathExtractor()
    j_1 = j.extract(query='data.forecast[1].date', body=res.text)
    j_2 = j.extract(query='data.ganmao', body=res.text)
    print(j_1, j_2)