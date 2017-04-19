# __author__ = 'zhangzhiyuan'
#-*-coding:utf-8-*-

import commands
'''
================说明===================
功能:启动uiantomatorviewer,查看app页面元素信息
======================================
'''
(status, output) = commands.getstatusoutput('open /Users/zzy/Documents/android-sdk-macosx/tools/uiautomatorviewer')
# 查看当前activity命令
# adb shell dumpsys activity | grep "mFocusedActivity"
# windows
# adb shell dumpsys activity | findstr "mFocusedActivity"