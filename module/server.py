#—*-coding:utf-8-*-
#启动\关闭appium服务,针对可以命令行执行appium服务
import os
import re
import signal
import ConfigParser
import subprocess
import commands
import logging
import sys


class Appium_server(object):

	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.read(os.path.dirname(sys.path[0]).split('test_case')[0] + "data/config.ini")
		self.appium_port = config.get('APPCONFIG','appium_port')
		self.bp_port = config.get('APPCONFIG','bp_port')
		self.udid = config.get('APPCONFIG','udid')
		self.appium_log = os.path.dirname(sys.path[0]).split('test_case')[0] + "data/appium_log.txt"

	def start_appium(self):
		cmd = 'appium -a 127.0.0.1 -p %s -bp %s -U %s>%s' %(self.appium_port,self.bp_port,self.udid,self.appium_log)
		logging.info('启动appium_server:'+ cmd)
		try:
			self.p = subprocess.Popen(cmd,shell=True)
		except BaseException as e:
			logging.error('启动appium_server失败')
			raise e


	def stop_appium(self):
		logging.info('停止appium_server')
		output = commands.getoutput('lsof -i :4723 |grep LISTEN')
		# print output
		PID = re.compile('\s+(\d+)\s+').search(output).group(1)
		# print PID
		try:
			os.kill(int(PID), signal.SIGKILL)
			print('已结束PID为%s的appium服务进程,' %PID)
		except OSError:
			print('没有如此进程!!!')

if __name__ == '__main__':
	T = Appium_server()
	T.start_appium()
	T.stop_appium()