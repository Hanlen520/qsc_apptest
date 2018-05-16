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

def Driver():
    config = Config()
    desired_caps = {'platformName': config.platform_name,
                    'platformVersion': config.platform_version,
                    'deviceName': config.device_name,
                    'appPackage': config.app_package,
                    'appActivity': config.app_activity,
                    'unicodeKeyboard': config.unicode_keyboard,
                    'resetKeyboard': config.reset_keyboard}
    appium_port = config.appium_port

    try:
        driver = webdriver.Remote('http://127.0.0.1:'+appium_port+'/wd/hub', desired_caps)
        logging.info('app启动成功!')
        return driver
    except BaseException as e:
        logging.error('app启动失败!' + str(e))
        print(e)
        return None

if __name__ == '__main__':
    dr = Driver()


