# __author__ = 'zhangzhiyuan'
#-*-coding:utf-8-*-
import commands
import ConfigParser
import os
import MySQLdb
import re
import signal
import subprocess
'''
================说明===================
功能:连接&断开测试机,查看devices状态
======================================
'''
def devices():
	f_ini = os.path.dirname(__file__).split('test_case')[0] + 'data/config.ini'
	config = ConfigParser.ConfigParser()
	config.read(f_ini)
	# 获取设备名称（通过命令行传入到config.ini）
	name = config.get('APPCONFIG','name')
	conn = MySQLdb.connect(host='172.16.10.83', user='root',
						   passwd='12345678', db='myweb', port=3306)
	conn.set_character_set('utf8')
	with conn:
		cur = conn.cursor()
    	#通过读取config.ini文件中的设备名称，执行sql命令，从数据库中获取对应设备型号和安卓版本
    	sql = 'select deviceName,platformVersion,appiumPort,bootstrapPort,udid,resolution from a_device where name = "%s"' % name
    	cur.execute(sql)
    	#获取设备型号、安卓版本、appium启动端口信息、设备udid
    	s = cur.fetchone()
    	deviceName = s[0]
    	platformVersion = s[1]
    	appium_port = s[2]
    	bp_port = s[3]
    	udid = s[4]
    	resolution = s[5]
    #将数据库中获取的设备相关信息写入config.ini
	config.set('APPCONFIG','appium_port',appium_port)
	config.set('APPCONFIG','bp_port',bp_port)
	config.set('APPCONFIG','udid',udid)
	config.set('APPCONFIG','deviceName',deviceName)
	config.set('APPCONFIG','platformVersion',platformVersion)
	config.set('APPCONFIG','resolution',resolution)

	with open(f_ini,"w+") as f:
		config.write(f)


	#adb连接设备,如果设备为无线连接
	if ':' in udid:
		cmd = 'adb connect %s' %udid
		#执adb connect 'udid'
		output = commands.getoutput(cmd)
		#Windows环境
		# output = os.popen(cmd).read()
		# print output
		#查看设备连接信息
		output2 = commands.getoutput('adb devices')
		# output2 = os.popen('adb devices').read()
		# print output2
		str1 = 'connected to %s' %udid
		str2 = '%s\tdevice' %udid
		try:
			if str1 in output:
				if str2 in output2:
					print '无线设备连接成功！'
					return True
				else:
					print output2+'\n设备连接失败,尝试重新连接......'
					raise OSError
			else:
				print output
				return False
		except OSError:
			commands.getoutput('adb disconnect ' + udid)
			# os.popen('adb disconnect ' + udid).read()
			output = commands.getoutput('adb connect ' + udid)
			# output = os.popen('adb connect ' + udid).read()
			output2 = commands.getoutput('adb devices')
			# output2 = os.popen('adb devices').read()
			if str1 in output:
				if  str2 in output2:
					print '设备连接成功！'
					return True
				else:
					print output2
					print '设备连接失败，请重启手机无线调试模式'
					return False
	elif 'device' in commands.getoutput('adb devices'): # os.popen('adb devices').read()
		print '有线设备连接成功！'
		return True
	else:
		print 'udid格式不正确！'
		return False

if __name__ == '__main__':
    devices()
