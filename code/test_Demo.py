#coding=utf-8
from appium import webdriver
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.qingsongchou.social'
desired_caps['appActivity'] = '.ui.activity.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
print driver.current_context

time.sleep(8)
driver.quit()