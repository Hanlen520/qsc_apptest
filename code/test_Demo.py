#coding=utf-8
from appium import webdriver
import time

desired_caps = {'platformName': 'Android', 'platformVersion': '7.0', 'deviceName': 'Android Emulator',
                'appPackage': 'com.android.calculator2', 'appActivity': '.Calculator '}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# driver.swipe(100,100,100,400)
driver.find_element_by_android_uiautomator('new UiSelector().text("6")').click()
driver.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
driver.find_element_by_android_uiautomator('new UiSelector().text("2")').click()
driver.find_element_by_id('com.android.calculator2:id/op_add').click()
driver.find_element_by_android_uiautomator('new UiSelector().text("2")').click()
driver.find_element_by_android_uiautomator('new UiSelector().text("4")').click()
driver.find_element_by_id('com.android.calculator2:id/eq').click()

time.sleep(8)
driver.quit()