#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64

from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from YDMHTTP import identify
import time

chromedriver = "D:\python\chromedriver.exe"
browser = webdriver.Chrome(chromedriver)
browser.get("https://kyfw.12306.cn/otn/resources/login.html")
time.sleep(2)
account_login = browser.find_element_by_xpath("//ul[@class='login-hd'] /li[@class='login-hd-account']").click()
time.sleep(1)
account = browser.find_element_by_id("J-userName").send_keys('你的账号')
password = browser.find_element_by_id("J-password").send_keys("你的密码")
page_source = browser.page_source
selector = etree.HTML(page_source) # 需要拿取页面图片数据
imageData = selector.xpath("//img[@class='imgCode']/@src")[0]
if len(imageData) > 0:
	#保存验证码为图片文件
	imageData = imageData.split(",")
	imageDataBytes = base64.b64decode(imageData[1])
	filepath = "./vcode.png"
	with open(filepath, "wb") as fp:
		fp.write(imageDataBytes)
	result = identify("vcode.png")
	print(result) # 返回确认图片的编号1-8的字符串, 例如'124'
	if (len(result) > 1):
		code_xy = [[60, 80], [120, 80], [180, 80], [270, 80], [60, 150], [120, 150], [180, 150], [270, 150]] # 手动确认的8个图片的中心点
		numbers = result[1]
		# 根据id为J-loginImg的标签相对位置点击对应验证码图片
		loginImgArea = browser.find_element_by_id("J-loginImg")
		for number in numbers:
			xy = code_xy[int(number) - 1]
			offset_x = xy[0]
			offset_y = xy[1]
			ActionChains(browser).move_to_element_with_offset(loginImgArea, offset_x, offset_y).click().perform()
		time.sleep(2)
		login_button = browser.find_element_by_id('J-login')
		login_button.click()



