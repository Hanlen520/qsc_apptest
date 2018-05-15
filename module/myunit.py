# __author__ = 'zhangzhiyuan'
#-*-coding:utf-8-*-
from .common import logger
from selenium import webdriver
from .driver import Driver
from .connect_devices import devices
from .server import Appium_server
import unittest
import logging
import sys
import time

'''
=====================说明======================
功能:自定义unittest框架,编写公用函数setup(),tearDown()
================================================
'''
class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #连接设备
        if devices():
            logger.info('设备连接成功！')
            # 启动appium_server
            cls.APPIUM = Appium_server()
            cls.APPIUM.start_appium()
            time.sleep(2)
            cls.driver = Driver()
            if cls.driver:
                logger.info('appium连接成功')
                cls.driver.implicitly_wait(15)
            else:
                logger.error('appium连接失败')
                cls.APPIUM.stop_appium()
                sys.exit()
        else:
            logger.error('连接设备失败')
            sys.exit()
    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
            logging.info('app退出成功!')
        except BaseException as e:
            logging.error('app退出失败!' + str(e))

        try:
            cls.APPIUM.stop_appium()
        except BaseException as e:
            logging.error('appium_server 停止失败！' + str(e))

if __name__ == '__main__':
    unittest.main()
