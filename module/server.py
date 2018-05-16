#—*-coding:utf-8-*-
#启动\关闭appium服务,针对可以命令行执行appium服务
from qsc_apptest.config.configure import Config
import os
import re
import signal
import subprocess
import commands
import logging


class Appium_server(object):

	def __init__(self,appium_port = None,bp_port = None,uuid = None):
		config = Config()
		if appium_port is None:
			self.appium_port = config.appium_port
		else:
			self.appium_port = appium_port
		if bp_port is None:
			self.bp_port = config.bp_port
		else:
			self.bp_port = bp_port
		if uuid is None:
			self.uuid = config.uuid
		else:
			self.uuid = uuid
		self.appium_log = config.appium_log

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