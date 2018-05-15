# __author__ = 'zzy'
#-*- coding:utf-8 -*-
from qsc_apptest.module.common import logger
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from fractions import Fraction
from qsc_apptest.config.configure import Config
import sys,importlib,time
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except ImportError:
    importlib.reload(sys)

class Element(object):
    """
    页面基础类，用于所有页面的继承
    """
    def __init__(self,driver):
        config = Config()
        self.driver = driver
        self.timeout = 30
        self.app_package = config.apppackage
        self.app_activity = config.appactivity

    def StartAppActivity(self,app_package,app_activity):
        self.driver.start_activity(app_package,app_activity)
        assert self.on_page(),'Did not land on %s' % self.app_activity

    def findElement(self,*loc):
        return self.driver.find_element(*loc)

    def findElements(self,*loc):
        return self.driver.find_elements(*loc)

    def getElement(self,elementDict):
        logger.info('开始定位元素')
        try:
            if elementDict['pathType'] == 'id':
                if 'index' in elementDict:
                    element = self.find_elements(By.ID,elementDict['pathValue'])
                    if element:
                        logger.info('id定位成功')
                        return element[int(elementDict['index'])]
                    else:
                        logger.error('id定位失败')
                        return None
                else:
                    element = self.find_element(By.ID,elementDict['pathvalue'])
                    if element:
                        logger.info('id定位成功')
                        return element
                    else:
                        logger.error('id定位失败')
                        return None

            if elementDict['pathType'] == 'name':
                element = self.driver.find_element_by_android_uiautomator('new UiSelector().text("' + elementDict['pathValue'] + '")')
                if element:
                    logger.info('name定位成功')
                    return element
                else:
                    logger.error('name定位失败')
                    return None

            if elementDict['pathType'] == 'class':
                if 'index' in elementDict:
                    element = self.find_elements(By.CLASS_NAME, elementDict['pathValue'])[int(elementDict['index'])]
                    if element:
                        logger.info('class定位成功')
                        return element
                    else:
                        logger.error('class定位失败')
                        return None
                else:
                    element = self.find_element(By.CLASS_NAME, elementDict['pathValue'])
                    if element:
                        logger.info('class定位成功')
                        return element
                    else:
                        logger.error('class定位失败')
                        return None
            if elementDict['pathType'] == 'coordinate':
                    logger.info('coordinate定位成功')
                    return elementDict

        except Exception as e:
            logger.error('{0}:元素定位失败'.format(e))
            return None

    def on_page(self):
        return self.driver.current_activity == self.app_activity

    def script(self,src):
        return self.driver.execute_script(src)

    def Tag(self,x,y,duration):
        time.sleep(2)
        action = TouchAction(self.driver)
        try:
            if duration:
                duration = duration * 1000
                action.long_press(x=x, y=y, duration=duration).release()
            else:
                # TouchAction(self.driver).press(None, x, y).release().perform()
                action.tap(x=x, y=y)
            action.perform()
            return True
        except BaseException as e:
            print(e)
            return False

    def Swipe2(self,start_x, start_y, end_x, end_y, duration=200):
        time.sleep(3)
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            return True
        except BaseException as e:
            print(e)
            return False

    def Swipe(self,direction,value,during=200):
        """
        swipe UP
        :param during:
        :return:
        """
        time.sleep(3)
        window_size = self.driver.get_window_size()
        width = window_size.get("width")
        height = window_size.get("height")
        if direction == 'down':
            i = Fraction(1) - Fraction(value)
            try:
                self.driver.swipe(width / 2, height * 3 / 4, width / 2, height * i.numerator / i.denominator, during)
                return True
            except Exception as e:
                print(e)
                return False
        elif direction == 'up':
            i = Fraction(value)
            try:
                self.driver.swipe(width / 2, height / 4 , width / 2, height * i.numerator / i.denominator, during)
                return True
            except Exception as e:
                print(e)
                return False
        elif direction == 'right':
            i = Fraction(1,4) + Fraction(value)
            try:
                self.driver.swipe(width / 4, height / 2, width * i.numerator / i.denominator , height / 2, during)
                return True
            except Exception as e:
                print(e)
                return False
        elif direction == 'left':
            i = (Fraction(3,4) - Fraction(value))
            try:
                self.driver.swipe(width * 3 / 4, height / 2, width * i.numerator / i.denominator, height / 2, during)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

if __name__ == '__main__':
