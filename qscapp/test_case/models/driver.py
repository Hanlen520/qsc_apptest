# __author__ = 'zhangzhiyuan'
# -*-coding:utf-8-*-

from appium import webdriver
from configobj import ConfigObj
import ConfigParser
import time
import os
import logging
import MySQLdb

'''
============说明==============
功能:app驱动文件
入口:驱动配置文件data/config.ini
=============================
'''

#driver驱动启动,返回driver
def app_genymotion():
    #读取配置驱动配置文件
    f_ini = os.path.dirname(__file__).split('test_case')[0] + 'data/config.ini'
    # readconfig = ConfigObj(f_ini)
    config = ConfigParser.ConfigParser()
    # config.readfp(open(f_ini))
    config.read(f_ini)

    desired_caps = {}
    desired_caps['platformName'] = config.get('APPCONFIG','platformName')
    desired_caps['platformVersion'] = config.get('APPCONFIG','platformVersion')
    desired_caps['deviceName'] = config.get('APPCONFIG','deviceName')
    desired_caps['appPackage'] = config.get('APPCONFIG','appPackage')
    desired_caps['appActivity'] = config.get('APPCONFIG','appActivity')
    desired_caps['unicodeKeyboard'] = config.get('APPCONFIG','unicodeKeyboard')
    desired_caps['resetKeyboard'] = config.get('APPCONFIG','resetKeyboard')
    # desired_caps['udid'] = config.get('APPCONFIG','udid')
    appium_port = config.get('APPCONFIG','appium_port')

    try:
        driver = webdriver.Remote('http://127.0.0.1:'+appium_port+'/wd/hub', desired_caps)
        logging.info('app启动成功!')
        return driver
    except BaseException,e:
        logging.error('app启动失败!' + str(e))
        print e
        return None

if __name__ == '__main__':
    dr = app_genymotion()
    try:
        dr.find_element_by_android_uiautomator('new UiSelector().text("发现")').click()
        dr.find_element_by_android_uiautomator('new UiSelector().text("小程序")').click()
        dr.find_element_by_android_uiautomator('new UiSelector().text("美团外卖+")').click()
        time.sleep(3)
        dr.switch_to.context("WEBVIEW_com.tencent.mm:tools")
    except:
        dr.quit()

