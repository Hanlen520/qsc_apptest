# __author__ = 'zhangzhiyuan'
# -*- coding:utf-8 -*-

from appium import webdriver
from qsc_apptest.config.configure import Config
import time
import os
import logging
import sys
try:
    import ConfigParser
except ModuleNotFoundError:
    from configparser import ConfigParser

"""
============说明==============
功能:app驱动文件
入口:驱动配置文件data/config.ini
=============================
"""

class Driver(object):

    def __init__(self,deviceInfo):
        self.config = Config()
        self.desired_caps = {'platformName': self.config.platform_name,
                        'platformVersion': self.config.platform_version,
                        'deviceName': self.config.device_name,
                        'appPackage': self.config.app_package,
                        'appActivity': self.config.app_activity,
                        'unicodeKeyboard': self.config.unicode_keyboard,
                        'resetKeyboard': self.config.reset_keyboard}
        self.appium_port = self.config.appium_port
        if deviceInfo is not None:
            self.desired_caps['platformVersion'] = deviceInfo['platformVersion']
            self.desired_caps['deviceName'] = deviceInfo['deviceName']

    def connect(self):
        try:
            driver = webdriver.Remote('http://127.0.0.1:'+ self.appium_port +'/wd/hub', self.desired_caps)
            logging.info('app启动成功!')
            return driver
        except BaseException as e:
            logging.error('app启动失败!' + str(e))
            print(e)
            return None

if __name__ == '__main__':
    dr = Driver()


