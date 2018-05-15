# -*- coding:utf-8 -*-
import xlrd
import logging
from logging.config import fileConfig
from logging.handlers import RotatingFileHandler
from lxml import etree
from qsc_apptest.config.configure import Config
import sys
class Common(object):

    def __init__(self):
        config = Config()
        self.log_txt = config.log_path   #配置日志文件位置
        self.f_xml = config.xml_path #配置xml文件位置
        self.f_xls = config.xls_path #配置xls文件位置
        self.img_expected = config.img_expected_path #配置预期截图文件位置
        self.img_actual = config.img_actual_path #配置实际截图文件位置
        self.img_path = config.img_path #配置上传图片路径
        # self.open_xml = etree.parse(self.f_xml)                             #将xml解析为树结构
        # self.open_xls = xlrd.open_workbook(self.f_xls, formatting_info=True)#打开xls文件
        self.host = config.db_host
        self.database = config.db_database
        self.username = config.db_name
        self.password = config.db_pass

        self.logg = fileConfig('logging.config')
        self.logger = logging.getLogger('root')
        # self.logger = logging.getLogger("qsc_apptest")
        # self.logger.setLevel(int(config.log_level))
        # #定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
        # rHandler = RotatingFileHandler(self.log_txt,maxBytes = 1*1024,backupCount = 3)
        # rHandler.setLevel(int(config.log_level))
        # formatter = logging.Formatter(fmt = config.fmt,datefmt = config.datefmt)
        # rHandler.setFormatter(formatter)
        #
        # console = logging.StreamHandler()
        # console.setLevel(int(config.log_level))
        # console.setFormatter(formatter)
        #
        # # 开启日志文件记录
        # if config.logfile_log_on == '1':
        #     self.logger.addHandler(rHandler)
        # # 开启控制台日志
        # if config.console_log_on == '1':
        #     self.logger.addHandler(console)

    @property
    def log(self):
        return self.logger


if __name__ == '__main__':
    C = Common()
    # print("你")
    C.logger.warning("sss")
    # print(sys.getdefaultencoding())

