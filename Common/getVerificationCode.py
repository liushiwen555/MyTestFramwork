# -*- coding: utf-8 -*-
# @Time     : 2021/7/2 9:00 下午
# @Author   : LiuShiWen


import json
import base64
import traceback
import requests
import pytesseract
from PIL import Image
from Common.getLog import logger
from Common.getConfig import Config
from selenium.webdriver.common.by import By
from time import sleep,strftime,localtime,time
from Library.baidu_api_sdk.aip import AipOcr
from Library.ShowapiRequest import ShowapiRequest


class IdentificationCodes(object):
    def __init__(self,driver=None,locationType=None,locatorExpression=None):
        """
        :param driver: 传入WebDriver实例
        :param locationType: 定位方式
        :param locatorExpression: 定位表达式
        """
        self.driver = driver
        self.locationType = locationType
        self.locatorExpression = locatorExpression
        self.config = Config()
        self.img_path = self.config.get_option_value('image', 'img_path')
        self.err_logger = logger('error')

    def get_code_img_path(self):
        st = strftime("%Y-%m-%d %H-%M-%S", localtime(time()))
        file_name = st + '.png'
        path = self.img_path
        '''设置保存整页截图的路径'''
        img_path = path + '/' + file_name
        self.driver.get_screenshot_as_file(img_path)
        try:
            '''定位到验证码'''
            code_location = self.driver.find_element(self.locationType,self.locatorExpression)
        except:
            self.driver.quit()
            self.err_logger.error(traceback.format_exc())
        '''获取定位到的验证码的左定点坐标'''
        left = code_location.location['x']
        top = code_location.location['y']
        '''获取验证码右底点坐标'''
        right = code_location.size['width'] + left
        height = code_location.size['height'] + top
        '''获取当前屏幕缩放比率系数，在后面抠图的时候传入'''
        dpr = self.driver.execute_script('return window.devicePixelRatio')
        '''打开前面整张截图文件，这里用到的是PILLOW图像包，需要安装PILLOW包，然后从PIL里导入Image'''
        im = Image.open(img_path)
        '''抠图，里面抠的位置是左定点坐标到右底点，然后都需要乘以当前屏幕分辨率的缩放系数dpr'''
        code_img = im.crop((left * dpr, top * dpr, right * dpr, height * dpr))
        code_img_path = path + '/' + st + 'code.png'
        '''将抠出的图片按照处理的路径保存'''
        code_img.save(code_img_path)
        '''二值化处理验证码图片'''
        code_image = Image.open(code_img_path)
        code_image = code_image.convert('L')
        threshold = 150
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        code_image = code_image.point(table, "1")
        # code_image.show()
        '''设置二值化后图片的保存路径'''
        binary_img_path = path + '/' + st + 'binary_code.png'
        code_image.save(binary_img_path)
        return binary_img_path

    def identify_verification_code_by_ttshitu(self):
        '''实例化获取处理后的二值化验证码'''
        code_img_path = self.get_code_img_path()
        def base64_api(img):
            with open(img, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                b64 = base64_data.decode()
                return b64

        b64 = base64_api(code_img_path)
        data = {"username": 'zhaoge555', "password": 'zhaoge555', "typeid": 3, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]

    def get_ttshitu_palance(self):
        urlget = "http://api.ttshitu.com/queryAccountInfo.json?username=zhaoge555&password=zhaoge555"
        result_get = requests.get(url=urlget).json()
        return result_get

    def identify_verification_code_by_ocr(self):
        code_img_path = self.get_code_img_path()
        # code_image.show()
        code = pytesseract.image_to_string(code_img_path)
        return code

    def identify_verification_code_by_ShowAI(self):
        code_img_path = self.get_code_img_path()
        '''调用第三方验证码识别AI的接口，将保存的验证码图片传进去，然后处理一下接口返回的数据，返回识别出的验证码'''
        r = ShowapiRequest("http://route.showapi.com/184-4", "272526", "a924d4e982ae404b8a068b4d1c7784f2")
        r.addFilePara("image", code_img_path)
        r.addBodyPara("typeId", "34")
        r.addBodyPara("convert_to_jpg", "0")
        r.addBodyPara("needMorePrecise", "0")
        res = r.post()
        text = res.json()['showapi_res_body']
        code = text['Result']
        return code

    def identify_verification_code_by_BaiduAI(self):
        """ 你的 APPID AK SK """
        APP_ID = '24445779'
        API_KEY = 'PnETgMU07BqkyWnm5PZRS52y'
        SECRET_KEY = 'e0seGaCUG31NK2YtgfUNUcNYNz4IX4tu'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        code_img_path = self.get_code_img_path()
        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return fp.read()
        code_image = get_file_content(code_img_path)
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        result = client.basicGeneral(code_image)
        # word_result = result.get('words_result')
        return result

def getCode(driver,locationType,locatorExpression):
    get_code = IdentificationCodes(driver,locationType,locatorExpression).identify_verification_code_by_ttshitu()
    return get_code

if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://localhost:8080/jpress/user/login")
    driver.maximize_window()
    code = IdentificationCodes(driver=driver,locationType=By.ID,locatorExpression="captcha-img").identify_verification_code_by_ttshitu()
    balance = IdentificationCodes().get_ttshitu_palance()
    # code = IdentificationCodes(driver, By.ID, "captcha-img").identify_verification_code_by_BaiduAI()
    print(code)
    print(balance)
    driver.quit()

    # driver = webdriver.Chrome()
    # driver.get("https://192.168.3.32")
    # sleep(10)
    # driver.maximize_window()
    # locator = '//*[@id="app"]/div/div/div[2]/div/div[2]/div[2]/form/div[3]/div/img'
    # # code = IdentificationCodes(driver=driver,locationType=By.XPATH,locatorExpression=locator).identify_verification_code_by_ttshitu()
    # code = getCode(driver,By.XPATH,locator)
    # print(code)