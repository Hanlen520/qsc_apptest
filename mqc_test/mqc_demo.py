# -*- coding: UTF-8 -*-

from appium import webdriver
from time import sleep
from unittest import TestCase
import unittest
import datetime
import desired_capabilities
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.touch_actions import TouchActions

class MqcTest(TestCase):

    global ratioX, ratioY
    global automationName
    global commandMap

    global caseName

    def setUp(self):
        desired_caps = desired_capabilities.get_desired_capabilities()
        uri = desired_capabilities.get_uri()
        retry = 0
        while retry < 3:
            try :
                self.driver = webdriver.Remote(uri, desired_caps)
                break
            except Exception, e:
                print "Appium server init failed: %s" % str(e)
                retry += 1

        sleep(10)
        self.init()

    def init(self):
        self.window_size  = self.driver.get_window_size()
        self.width = 1080
        self.height = 1920
        self.ratioX = float("%.2f" % (float(self.window_size["width"]) / float(self.width)))
        self.ratioY = float("%.2f" % (float(self.window_size["height"]) / float(self.height)))
        self.automationName = self.driver.capabilities.get('automationName')
        self.caseName = ""
        self.commandMap = {
            "swipe" : self.swipe,
            "click" : self.click,
            "longclick" : self.longclick,
            "tap" : self.tap,
            "longtap" : self.longtap,
            "keycode" : self.keycode,
            "send_text" : self.send_text,
            "sleep" : self.sleep
        }

    def test_firstcase(self):
        steps = [
                # 等待5秒
                ['sleep',5],
                # 左滑
                ['swipe', None, 'left'],
                # 左滑
                ['swipe', None, 'left'],
                # 左滑
                ['swipe', None, 'left'],
                # 点击控件：立即进入
                ['click', None, 'com.qingsongchou.social:id/bt_action', '立即进入', None, None, None],
                # 点击控件：com.qingsongchou.social:id/tab3
                ['click', None, 'com.qingsongchou.social:id/tab3', '', None, None, None],
                # 在控件 填写你的手机号 上输入 1111111111
                ['send_text', None, 'com.qingsongchou.social:id/et_number_input','11111111111' , None, '填写你的手机号'],
                # 点击控件：下一步
                ['click', None, None, '下一步', 352.0, 747.0, None],
                # 在控件 下一步 上输入 11111
                ['send_text', None, None, '11111', None, '填写5位验证码'],
                # 点击控件：登录
                ['click', None, 'com.qingsongchou.social:id/bt_login', '登录', 389.0, 795.0, None],'测试用例'
                ]
        self.drive(steps)


    #####################################################################################
    # this function drives the steps in cases.
    # It's more stable, more easier to expand.
    # Arguments:
    #   steps, an array contains all the actions data in each action. Each action contains
    #   commandType and command datas.
    #####################################################################################
    def drive(self, steps):
        i = 0
        continuous_fail_steps = 0
        while i < len(steps):
            self.log("step", "step %d begin, screenshot %s" % ((i+1), self.caseName + "_" + str(i+1)))
            step = steps[i]
            last_step = steps[i-1] if i > 0 else None
            next_step = steps[i+1] if i < len(steps)-1 else None
            retry = 0
            if len(step) > 0:
                while True:
                    try:
                        if retry < 2:
                            self.commandMap[step[0]](*step[1:])
                            continuous_fail_steps = 0
                            break
                        else :
                            #try to backward to former step and retry.
                            if last_step is not None:
                                try:
                                    self.commandMap[last_step[0]](*last_step[1:])
                                    self.commandMap[step[0]](*step[1:])
                                    continuous_fail_steps = 0
                                    break
                                except:
                                    pass
                    except Exception,e:
                        self.log("ERROR", str(e))

                    if retry < 2:
                        retry += 1
                    else:
                        continuous_fail_steps += 1
                        break

            #move to next step.
            self.screencap(self.caseName + "_" + str(i+1))
            if continuous_fail_steps != 0:
                self.log("FATAL", "step failed")
            i+=1

    def tearDown(self):
        ## Just ignore it. Cases are done.
        try:
            self.driver.quit()
        except:
            pass

    #########################################################
    # the flollowing code is command types' implementation.
    #########################################################
    def swipe(self, points, dir):
        if dir is not None:
            if dir == 'up':
                self.driver.swipe(self.window_size["width"] * 0.5, self.window_size["height"] * 0.2, self.window_size["width"] * 0.5, self.window_size["height"] * 0.8, 1000)
            elif dir == 'down':
                self.driver.swipe(self.window_size["width"] * 0.5, self.window_size["height"] * 0.8, self.window_size["width"] * 0.5, self.window_size["height"] * 0.2, 1000)
            elif dir == 'left':
                self.driver.swipe(self.window_size["width"] * 0.9, self.window_size["height"] * 0.5, self.window_size["width"] * 0.1, self.window_size["height"] * 0.5, 1000)
            elif dir == 'right':
                self.driver.swipe(self.window_size["width"] * 0.1, self.window_size["height"] * 0.5, self.window_size["width"] * 0.9, self.window_size["height"] * 0.5, 1000)
            return
        last_x = 0
        last_y = 0
        if self.automationName == 'Appium':
            action_appium = TouchAction(self.driver)
            for i in range(0, len(points)):
                x = float(points[i][0]) * self.ratioX
                y = float(points[i][1]) * self.ratioY
                if i == 0:
                    action_appium = action_appium.press(None, x, y).wait(20)
                elif i == (len(points) - 1):
                    action_appium = action_appium.move_to(None, x - last_x, y - last_y).wait(20).release()
                    action_appium.perform()
                else:
                    action_appium = action_appium.move_to(None, x - last_x, y - last_y).wait(20)
                last_x = x
                last_y = y
        else:
            action_selendroid = TouchActions(self.driver)
            for i in range(0, len(points)):
                x = float(points[i][0]) * self.ratioX
                y = float(points[i][1]) * self.ratioY
                if i == 0:
                    action_selendroid.tap_and_hold(x, y)
                elif i == (len(points) - 1):
                    action_selendroid.move(x, y).release(x, y).perform()
                else:
                    action_selendroid.move(x, y)


    def click(self, xpath, resource_id, desc, x, y, index = None, isAssert = True):
        # trying to click xpath
        if (xpath is not None and (resource_id is None or resource_id == '') and "android.webkit.WebView" in xpath):
            if x>0 and y>0:
                try:
                    self.tap(x,y)
                    return True
                except:
                    pass
            raise Exception("click point (%d, %d) failed" % (x, y))
        elif (xpath is not None and xpath != '') or \
           (resource_id is not None and resource_id != '') or \
           (desc is not None and desc != ''):
            try:
                self.wait_for_element(xpath=xpath, id=resource_id, text=desc, index=index).click()
                if isAssert :
                    self.log("assert", "true")
                return True
            except:
                pass
            if isAssert :
                self.log("assert", "false")
            raise Exception("click element id[%s] text[%s] not found" % (resource_id, desc))
        else:
            #trying to click position
            if x>0 and y>0:
                try:
                    self.tap(x,y)
                    return True
                except:
                    pass
            raise Exception("click point (%d, %d) failed" % (x, y))

    def longclick(self, xpath, resource_id, desc, x, y, index = None, time = 5, isAssert = True):
        # trying to click xpath
        if (xpath is not None and (resource_id is None or resource_id == '') and "android.webkit.WebView" in xpath):
            if x>0 and y>0:
                try:
                    self.longtap(x,y,time)
                    return True
                except:
                    pass
            raise Exception("click point (%d, %d) failed" % (x, y))
        elif (xpath is not None and xpath != '') or \
           (resource_id is not None and resource_id != '') or \
           (desc is not None and desc != ''):
            try:
                appium_action = TouchAction(self.driver)
                appium_element = self.wait_for_element(xpath=xpath, id=resource_id, text=desc, index=index)
                appium_action.long_press(appium_element, None, None, time * 1000).perform()
                if isAssert :
                    self.log("assert", "true")
                return True
            except:
                pass
            if isAssert :
                self.log("assert", "false")
            raise Exception("click element id[%s] text[%s] not found" % (resource_id, desc))
        else:
            #trying to click position
            if x>0 and y>0:
                try:
                    self.longtap(x,y,time)
                    return True
                except:
                    pass
            raise Exception("click point (%d, %d) failed" % (x, y))

    def tap(self, x, y):
        x = float(x) * self.ratioX
        y = float(y) * self.ratioY
        if self.automationName == 'Appium' :
            TouchAction(self.driver).press(None, x, y).release().perform()
        else:
            TouchActions(self.driver).tap_and_hold(x, y).release(x, y).perform()

    def longtap(self, x, y, time = 5):
        x = float(x) * self.ratioX
        y = float(y) * self.ratioY
        if self.automationName == 'Appium' :
            TouchAction(self.driver).long_press(None, x, y, time * 1000).perform()
        else:
            TouchActions(self.driver).tap_and_hold(x, y).wait(time * 1000).release(x, y).perform()

    def keycode(self, codes):
        try :
            if self.automationName == 'Appium':
                for a, b in codes:
                    self.driver.press_keycode(a, b)
            else:
                for a, b in codes:
                    self.driver.keyevent(a, b)
        except :
            return False
        return True

    def keycodeChar(self, char):
        try :
            if char.isdigit():
                self.driver.press_keycode(int(char) + 7, None)
            else:
                meta = None
                if char.isupper():
                    meta = 1
                    char = char.lower()
                self.driver.press_keycode(ord(char)-ord('a')+29, meta)
        except :
            return False
        return True

    def send_text(self, xpath, resource_id, input, index=None, desc=None):
        try:
            if (xpath is not None and (resource_id is None or resource_id == '') and "android.webkit.WebView" in xpath):
                for i, ch in enumerate(input):
                    self.keycodeChar(ch)
            else :
                self.wait_for_element(xpath = xpath, id = resource_id, text = desc, index = index).send_keys(input.decode('UTF-8'))
            return True
        except:
            raise Exception("send text id[%s] text[%s] not found" % (id, resource_id))

    def sleep(self, time):
        sleep(time)

    ###############################################
    # the following are private codes.
    ###############################################
    def id(self, resource_id):
        if self.automationName == 'Appium':
            return resource_id
        else:
            return resource_id.split('/')[1]

    def screencap(self, picName=None):
        try:
            if picName is not None:
                self.log("screenshot", picName)
            else:
                self.log("screenshot", " ")
            sleep(3)
        except:
            pass

    def log(self, level, info):
        print "%s : %s" % (level, info)
        desired_capabilities.flushio()

    def wait_for_element(self, xpath=None, id=None, text=None, index=None):
        time = 0
        while True:
            # try to find element by xpath.
            try:
                if xpath is not None:
                    el = self.driver.find_element_by_xpath(xpath)
                    self.log("info", "Find element with xpath success")
                    return el
            except:
                pass

            # try to find element by id.
            try:
                if id is not None:
                    if index is not None:
                        return self.driver.find_elements_by_id(self.id(id))[index]
                    else:
                        return self.driver.find_element_by_id(self.id(id))
            except:
                pass

            # try to find element by text.
            try:
                if text is not None:
                    if self.automationName == 'Appium':
                        return self.driver.find_element_by_android_uiautomator(
                            'new UiSelector().textContains("' + text + '")')

                    else:
                        return self.driver.find_element_by_link_text(text)
            except:
                pass

            sleep(1)
            time += 1
            if time > 10:
                raise Exception("Element id[%s] text[%s] not found in %d times" % (id, text, time))
                break

    def floatrange(self, start, stop, steps):
        return [start + float(i) * (stop - start) / (float(steps) - 1) for i in range(steps)]

if __name__ == '__main__':
    try: unittest.main()
    except SystemExit: pass
