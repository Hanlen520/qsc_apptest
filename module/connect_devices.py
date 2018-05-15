#!/usr/bin/python
# -*- coding:utf-8 -*-
from .common import Config
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
		#Windows环境
		# output = os.popen(cmd).read()
		# print output
		#查看设备连接信息
		output2 = ExecuteCMD("adb devices")
		# output2 = os.popen("adb devices").read()
		# print output2
		str1 = "connected to %s" %udid
		str2 = "%s\tdevice" %udid
		try:
			if str1 in output:
				if str2 in output2:
					print("无线设备连接成功！")
					return True
				else:
					print("{0}\n设备连接失败,尝试重新连接......".format(output2))
					raise OSError
			else:
				print(output)
				return False
		except OSError:
			ExecuteCMD("adb disconnect " + udid)
			# os.popen("adb disconnect " + udid).read()
			output = ExecuteCMD("adb connect " + udid)
			# output = os.popen("adb connect " + udid).read()
			output2 = ExecuteCMD("adb devices")
			# output2 = os.popen("adb devices").read()
			if str1 in output:
				if  str2 in output2:
					print ("设备连接成功！")
					return True
				else:
					print(output2)
					print("设备连接失败，请重启手机无线调试模式")
					return False
	elif "device" in ExecuteCMD("adb devices"): # os.popen("adb devices").read()
		print("有线设备连接成功！")
		return True
	else:
		print("udid格式不正确！")
		return False


def ExecuteCMD(shell):
	if sys.version_info >= (3,3):
		result = subprocess.check_output(shell)
	else:
		result = commands.getoutput(shell)
	return result

if __name__ == "__main__":
	devices()
