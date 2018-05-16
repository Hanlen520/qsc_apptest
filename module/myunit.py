# __author__ = 'zhangzhiyuan'
#-*-coding:utf-8-*-
from .common import logger,Common
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

    DEVICE_NAME = None
    DRIVER = None
    APPIUM = None

    def __init__(self,methodName = 'runTest',deviceName = None):
        super(MyTest,cls).__init__(methodName)
        self.DEVICE_NAME = deviceName

    @classmethod
    def setUpClass(cls):
        #连接设备
        if cls.DEVICE_NAME is not None:
            logger.info('设备连接成功！')
            deviceInfo = Common().GetDevices(cls.DEVICE_NAME)
            # 启动appium_server
            cls.APPIUM = Appium_server(deviceInfo['appium_port'],deviceInfo['bp_port'],deviceInfo['uuid']).start_appium()
            time.sleep(2)
            cls.DRIVER = d.Driver(deviceInfo).connect()
            if cls.DRIVER:
                logger.info('appium连接成功')
                cls.DRIVER.implicitly_wait(15)
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
            cls.DRIVER.quit()
            logging.info('app退出成功!')
        except BaseException as e:
            logging.error('app退出失败!' + str(e))

        try:
            cls.APPIUM.stop_appium()
        except BaseException as e:
            logging.error('appium_server 停止失败！' + str(e))

if __name__ == '__main__':
    unittest.main()
