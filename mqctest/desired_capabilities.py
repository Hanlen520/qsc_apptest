#!/usr/bin/env python
import sys
def get_desired_capabilities():
  desired_caps = {
    "platformName": "Android",
    "platformVersion": "6.0.1",
    "deviceName": "MQC",
    "udid": "10.0.0.221:5555",
    "appPackage": "com.qingsongchou.social",
    "appWaitPackage": "com.qingsongchou.social",
    "app": "/Users/zzy/Downloads/qingsongchou/qingsongchou.apk",
    "newCommandTimeout": 30,
    "automationName": "Appium",
    "unicodeKeyboard": True,
    "resetKeyBoard": True
  }

  return desired_caps

def get_uri():
  return "http://localhost:4723/wd/hub"
def get_username():
  return "11111111111"
def get_password():
  return "11111"
def flushio():
    sys.stdout.flush()
