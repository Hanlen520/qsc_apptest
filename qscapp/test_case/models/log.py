#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''实现功能：
支持自由配置,如下log.conf,
1）可以配置日志文件路径(log_file)；
2）按日志数量配置(backup_count)及单个日志文件的大小(max_bytes_each）,自动化循环切换日志文件；
3）支持日志格式自定义(fmt)；
4）支持日志记录器名称自定义(logger_name)
6）支持控制台日志和文件日志
5) 支持控制台日志级别自定义(log_level_in_console)
6）支持文件日志级别自定义(log_level_in_logfile)
7) 支持控制台和文件日志的各自的开启和关闭(分别为console_log_on, logfile_log_on)
'''
import logging
import os
import time
from logging.handlers import RotatingFileHandler
import threading
from configobj import ConfigObj

class LogSignleton(object):
    def __init__(self):
        pass

    def __new__(cls):
        mutex=threading.Lock()
        mutex.acquire() # 上锁，防止多线程下出问题
        if not hasattr(cls, 'instance'):
            cls.instance = super(LogSignleton, cls).__new__(cls)
            now = time.strftime("%Y-%m-%d %H_%M_%S")
            log_config = os.getcwd().split('test_case')[0] + 'data/log_config.ini'
            config = ConfigObj(log_config)
            # config = configparser.ConfigParser()
            # config.read(log_config)
            cls.instance.log_filename = config['LOGGING']['log_file'] + now + 'log.txt'
            cls.instance.max_bytes_each = int(config['LOGGING']['max_bytes_each'])
            cls.instance.backup_count = int(config['LOGGING']['backup_count'])
            cls.instance.fmt = config['LOGGING']['fmt']
            cls.instance.log_level_in_console = int(config['LOGGING']['log_level_in_console'])
            cls.instance.log_level_in_logfile = int(config['LOGGING']['log_level_in_logfile'])
            cls.instance.logger_name = config['LOGGING']['logger_name']
            cls.instance.console_log_on = int(config['LOGGING']['console_log_on'])
            cls.instance.logfile_log_on = int(config['LOGGING']['logfile_log_on'])
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance

    def get_logger(self):
        return  self.logger

    def __config_logger(self):
        # 设置日志格式
        fmt = self.fmt.replace('|','%')
        formatter = logging.Formatter(fmt)

        if self.console_log_on == 1: # 如果开启控制台日志
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            self.logger.setLevel(self.log_level_in_console)

        if self.logfile_log_on == 1: # 如果开启文件日志
            rt_file_handler = RotatingFileHandler(self.log_filename, maxBytes=self.max_bytes_each, backupCount=self.backup_count)
            rt_file_handler.setFormatter(formatter)
            self.logger.addHandler(rt_file_handler)
            self.logger.setLevel(self.log_level_in_logfile)

if __name__ == '__main__':

    logsignleton = LogSignleton()
    logger = logsignleton.get_logger()
    # logger = logging.getLogger('apptest_log') # 在其它模块中时，可这样获取该日志实例
    logger.debug('this is a debug level message')
    logger.info('this is info level message')
    logger.warning('this is warning level message')
    logger.error('this is error level message')
    logger.critical('this is critical level message1')
    logger.critical('this is critical level message2')
    logger.critical('this is critical level message3')