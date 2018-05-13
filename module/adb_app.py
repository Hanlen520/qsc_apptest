# __author__ = 'zhangzhiyuan'
#-*-coding:utf-8-*-

#功能:获取app的activity页面

import commands
import re,sys
import driver



app_name = 'com.qingsongchou.social'

(status, output) = commands.getstatusoutput('adb shell dumpsys package '+app_name)

activity = re.compile(r'com.qingsongchou.social/.ui.activity.'+'(.*)'+'filter')
#获取app的activity页面
s = activity.findall(output)
#去重,并排序(保持原来的顺序)
for app_activity in sorted(set(s),key = s.index):
    print app_activity
    # dr = driver.app_genymotion(app_activity)
    # dr.quit()

#打印activity页面总数
# print len(sorted(set(s),key = s.index))
# adb shell dumpsys activity activities显示当前activity