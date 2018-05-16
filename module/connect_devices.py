#!/usr/bin/python
# -*- coding:utf-8 -*-
from .common import Config
from .common import ExecuteCMD
from .common import logger
try:
	import commands
except ModuleNotFoundError:
	import subprocess
import sys
try:
	import ConfigParser
except ModuleNotFoundError:
	import configparser as ConfigParser

"""
================说明===================
功能:连接&断开测试机,查看devices状态
======================================
"""
def devices():


	config = Config()
	config.setConfig("APP","appium_port",appium_port)
	# 将数据库中获取的设备相关信息写入config.ini
	config.set("APPCONFIG","appium_port",appium_port)
	config.set("APPCONFIG","bp_port",bp_port)
	config.set("APPCONFIG","udid",udid)
	config.set("APPCONFIG","deviceName",deviceName)
	config.set("APPCONFIG","platformVersion",platformVersion)
	config.set("APPCONFIG","resolution",resolution)

	with open(f_ini,"w+") as f:
		config.write(f)

	#adb连接设备,如果设备为无线连接
	if ":" in udid:
		cmd = "adb connect %s" %udid
		output = ExecuteCMD(cmd)
		#查看设备连接信息
		output2 = ExecuteCMD("adb devices")
		str1 = "connected to %s" %udid
		str2 = "%s\tdevice" %udid
		try:
			if str1 in output:
				if str2 in output2:
					logger("无线设备连接成功！")
					return True
				else:
					logger.info("{0}\n设备连接失败,尝试重新连接......".format(output2))
					raise OSError
			else:
				logger.info(output)
				return False
		except OSError:
			ExecuteCMD("adb disconnect " + udid)
			output = ExecuteCMD("adb connect " + udid)
			output2 = ExecuteCMD("adb devices")
			if str1 in output:
				if  str2 in output2:
					logger.info("设备连接成功！")
					return True
				else:
					logger.error(output2)
					logger.error("设备连接失败，请重启手机无线调试模式")
					return False
	elif "device" in ExecuteCMD("adb devices"): # os.popen("adb devices").read()
		logger.info("有线设备连接成功！")
		return True
	else:
		logger.info("udid格式不正确！")
		return False


if __name__ == "__main__":
	devices()
