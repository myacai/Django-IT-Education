# coding:u8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64
import re
import time


class Demo():
    def __init__(self):
        self.coordinate = [[-105, -20], [-35, -20], [40, -20], [110, -20], [-105, 50], [-35, 50], [40, 50], [110, 50]]

    def login(self):
        login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        print("启动浏览器，打开12306")
        webdriverUrl = r'D:\a桌面\myGithub\Django-IT-Education\pythonWeb\education_project\爬虫\login12306\chromedriver.exe'
        driver = webdriver.Chrome(webdriverUrl)
        # driver = webdriver.Chrome()
        driver.set_window_size(1200, 900)
        driver.get(login_url)
        account = driver.find_element_by_class_name("login-hd-account")
        account.click()
        userName = driver.find_element_by_id("J-userName")
        userName.send_keys("cai115264")
        password = driver.find_element_by_id("J-password")
        password.send_keys("1152641262cai")
        self.driver = driver

    def getVerifyImage(self):
        try:

            img_element = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "J-loginImg"))
            )

        except Exception as e:
            print(u"网络开小差,请稍后尝试")
        base64_str = img_element.get_attribute("src").split(",")[-1]
        imgdata = base64.b64decode(base64_str)
        with open('verify.jpg', 'wb') as file:
            file.write(imgdata)
        self.img_element = img_element

    def getVerifyResult(self):
        url = "http://littlebigluo.qicp.net:47720/"
        response = requests.request("POST", url, data={"type": "1"}, files={'pic_xxfile': open('verify.jpg', 'rb')})
        result = []
        print(response.text)
        for i in re.findall("<B>(.*)</B>", response.text)[0].split(" "):
            result.append(int(i) - 1)
        self.result = result
        print(result)

    def moveAndClick(self):
        try:
            Action = ActionChains(self.driver)
            for i in self.result:
                Action.move_to_element(self.img_element).move_by_offset(self.coordinate[i][0],
                                                                        self.coordinate[i][1]).click()
            Action.perform()
        except Exception as e:
            print(e.message())

    def submit(self):
        self.driver.find_element_by_id("J-login").click()

    def __call__(self):
        self.login()
        time.sleep(3)
        self.getVerifyImage()
        time.sleep(1)
        self.getVerifyResult()
        time.sleep(1)
        self.moveAndClick()
        time.sleep(1)
        self.submit()
        time.sleep(10000)


Demo()()
