# __author__ = 'vistest'
# -*-coding:utf-8-*-
import sys
import os
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from models.base import Page
from models.log import LogSignleton
import logging
'''
===========说明==============
功能:页面元素定位功能
入口:页面元素信息表xml文件
============================
'''

class homepage(Page):

    # hompage_table_loc = (By.CLASS_NAME, "android.widget.TextView")

    def home_elements(self,activity,name):
        return self.get_xml(activity, name)
