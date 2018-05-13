# __author__ = 'vistest'
#-*-coding:utf-8-*-
import os
import zipfile
import time
import re

# 连接手机
def connect_phone():
    os.system('adb connect 10.0.0.221')
    os.system('adb devices')

# 清除应用数据
def clean_apk():
    os.system('adb shell pm clear com.qingsongchou.social')

# 获取所有输入法
def get_input():
    os.system('adb shell ime list -s')

# 获取默认输入法
def get_default_input():
    os.system('adb shell settings get secure default_input_method')

# 设置默认输入法
def set_input():
    os.system('adb shell ime set com.sohu.inputmethod.sogou.xiaomi/.SogouIME')

# 安装应用
def install_apk():
    os.system('adb install -r ')

# 卸载应用
def uninstall_apk():
    os.system('adb uninstall com.qingsongchou.social')

# 查看当前activity命令
def get_activity():
    os.system('adb shell dumpsys activity | grep "mFocusedActivity" ')

# 查看所有包名
def get_packages():
    os.system('adb shell pm list packages | grep ""')

# 查看应用信息
def get_package_information():
    os.system('adb shell dumpsys package com.qingsongchou.social | egrep "versionName|firstInstallTime"')

#monkey测试
def monkey_test():
    os.system('adb shell monkey -p com.qingsongchou.social -v 100')

#zip文件
def zip_file():
    # now = time.strftime("%m_%d_%H:%M")
    path = os.path.dirname(__file__) + '/build/'
    z = zipfile.ZipFile(path + 'main.py.zip','w')
    z.write('main.py')
    z.close()

# 计算坐标值
def point(s):
    value = re.compile('\[(.*?)\]')
    expected_value = value.findall(s)
    x = (int(expected_value[1].split(',')[0])-int(expected_value[0].split(',')[0]))/2+int(expected_value[0].split(',')[0])
    y = (int(expected_value[1].split(',')[1])-int(expected_value[0].split(',')[1]))/2+int(expected_value[0].split(',')[1])
    p = '(' + str(x) + ',' + str(y) + ')'
    print p
if __name__ == '__main__':
    connect_phone()
    # clean_apk()
    # get_input()
    # get_default_input()
    # set_input()
    # get_packages()
    # get_package_information()
    # zip_file()
    # get_activity()
    # point('[30,1398][300,1668]')