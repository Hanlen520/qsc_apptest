# __author__ = 'zhanghzhiyuan'
# -*- coding:utf-8 -*-

from myunit import MyTest
from base import Page
import unittest
import ConfigParser
import logging
import re,os
import time
from retrying import retry
import sys
"""
===========说明============
功能:测试用例执行
入口:ecxel表格测试用例
==========================
"""

class Testcase(Page):
    """测试用例基础类"""
    # loggeer = logging.getLogger('zzy')
    def __init__(self,driver,onecase,sheetname):
        super(Testcase,self).__init__()
        self.driver = driver
        self.testcase = onecase
        self.table = sheetname
        self.case_id = self.testcase['case_id']
        self.case_name = self.testcase['case_name']
        self.name = self.testcase['name']
        self.activity = self.testcase['activity']
        self.action = self.testcase['action']
        self.value = self.testcase['value']
        self.expected = self.testcase['expected']
        #获取设备分辨率
        f_ini = os.path.dirname(sys.path[0]).split('test_case')[0] + 'data/config.ini'
        config = ConfigParser.ConfigParser()
        config.read(f_ini)
        self.resolution = config.get('APPCONFIG','resolution')

    def get_expected(self,expected):
        if '【' not in expected and '.' in expected:
            return expected
        else:
            # 获取表格中'【 】'里面的的值,返回列表
            value = re.compile('【(.*?)】')
            expected_value = value.findall(str(expected))

            return expected_value

    def log(self,actual_value,results_value):
        #实际结果和执行情况写入表格,记录日志
        actual = self.set_mysql(self.table, self.case_id, 'actual', actual_value)
        results = self.set_mysql(self.table, self.case_id, 'results', results_value)
        if actual and results:
            logging.info('测试结果写入完成!<' + self.case_id + ':'+ results_value+'>')
        else:
            logging.info('测试结果写入失败')

    #失败重试1次
    def retry_if_ValueError_error(exception):
        return isinstance(exception, ValueError)

    @retry(wait_fixed = 5000,stop_max_attempt_number = 2,retry_on_exception = retry_if_ValueError_error)
    def execute_case(self):
        """执行测试用例"""
        loggeer = logging.getLogger('zzy')
        #-------------------------------------执行测试用例---------------------------------------
        loggeer.info('==========开始执行测试用例' + self.case_id + '===========')
        if self.action in ['click','sendkey','swipe','back','tag','sleep']:
            # 获取页面元素
            if self.activity:
                # if 'com' in self.activity:
                #     activity = self.activity
                # else:
                #     activity = '.ui.activity.' + self.activity
                # if self.driver.wait_activity(self.activity, 15, 1):
                element = self.get_element(self.get_xml(self.activity, self.name)) #判断页面中activity是否存在
                if element:
                    # 判断页面元素是否成功获取
                    if self.action == 'click':
                        self.before_activity = self.driver.current_activity
                        element.click()
                    elif self.action == 'sendkey':
                        try:
                            self.driver.hide_keyboard()
                        except BaseException:
                            # print '没有弹出键盘'
                            pass
                        # print self.value
                        element.clear()
                        if '"' in self.value:
                            if '，' in self.value:
                                self.value = self.value.replace('，',',')
                            element.send_keys(eval(self.value).decode('utf8'))
                        else:
                            element.send_keys(self.value.decode('utf8'))
                    elif self.action == 'swipe':
                        self.before_activity = self.driver.current_activity
                        #分辨率等比换算
                        ratioX = float("%.2f" % (float(element['resolution'].split('x')[0]) / float(self.resolution.split('x')[0])))
                        ratioY = float("%.2f" % (float(element['resolution'].split('x')[1]) / float(self.resolution.split('x')[1])))
                        start_x = float(element['start_x']) * ratioX
                        start_y = float(element['start_y']) * ratioY
                        end_x = float(element['end_x']) * ratioX
                        end_y = float(element['end_y']) * ratioY

                        try:
                            self.my_swipe2(start_x,start_y,end_x,end_y)
                        except BaseException:
                            logging.error('滑动失败')
                else:
                    self.log(u'页面元素无法定位','fail')
                    self.driver.quit()
                    self.insert_img(self.case_name + '.jpg')
                    raise ValueError('元素定位失败')
                # else:
                #     logging.error('当前activity为： '+ self.driver.current_activity)
                #     print self.activity
                #     self.insert_img(self.case_name + '.jpg')
                #     self.driver.quit()
                #     raise Warning('页面中没有当前activity:')


            else:
                logging.info('不解析xml文件,通过页面text定位元素')
                # print '%s,%s' %(self.case_id self.name)
                if self.action == 'click':
                    try:
                        # 获取执行操作的activity
                        self.before_activity = self.driver.current_activity
                        element = self.driver.find_element_by_android_uiautomator(
                            'new UiSelector().textContains("' + self.name + '")')
                        logging.info(u'点击' '【' + self.name + '】')
                        element.click()
                    except BaseException:
                        logging.error('元素定位失败')
                        self.log(u'页面元素无法定位', 'fail')
                        self.insert_img(self.case_name + '.jpg')
                        self.driver.quit()
                        raise ValueError('元素定位失败')


                elif self.action == 'sendkey':
                    try:
                        element = self.driver.find_element_by_android_uiautomator(
                            'new UiSelector().textContains("' + self.name + '")')

                    except BaseException,e:
                        print e
                        logging.error('元素定位失败')
                        self.log(u'页面元素无法定位', 'fail')
                        self.insert_img(self.case_name + '.jpg')
                        self.driver.quit()
                        raise ValueError('元素定位失败')

                    # try:
                    #     self.driver.hide_keyboard()
                    # except BaseException:
                    #     pass
                    if 'jpg' not in self.value:
                        element.clear()
                    logging.info(u'在' '【' + self.name + '】' + '输入:' + self.value)
                    if '"' in self.value:
                        if '，' in self.value:
                            self.value = self.value.replace('，',',')
                        element.send_keys(eval(self.value).decode('utf8'))
                    else:
                        element.send_keys(self.value.decode('utf8'))

                elif self.action == 'swipe':
                    self.before_activity = self.driver.current_activity
                    swipe_value = self.value.split(',')
                    try:
                        self.my_swipe(swipe_value[0], swipe_value[1])
                    except BaseException:
                        logging.error('滑动失败')
                elif self.action == 'tag':
                    self.before_activity = self.driver.current_activity
                    #获取点击坐标
                    if '，' in self.value:
                        self.value = self.value.replace('，',',')
                    tag_value = eval(self.value)
                    #判断是否存在长按时间
                    if len(tag_value) >2:
                        duration = tag_value[2]
                    else:
                        duration = None
                    tag_x = tag_value[0]
                    tag_y = tag_value[1]
                    #分辨率换算
                    ratioX = float("%.2f" % (float(1080) / float(self.resolution.split('x')[0])))
                    ratioY = float("%.2f" % (float(1920) / float(self.resolution.split('x')[1])))
                    #换算后的坐标
                    start_x = float("%.2f" % (float(tag_x) / ratioX))
                    start_y = float("%.2f" % (float(tag_y) / ratioY))
                    try:
                        self.my_tag(start_x,start_y,duration)
                    except BaseException:
                        logging.error('点击坐标失败')
                elif self.action == 'sleep':
                    time.sleep(int(self.value))
                elif self.action == 'back':
                    self.before_activity = self.driver.current_activity
                    try:
                        self.driver.press_keycode('4')
                    except BaseException:
                        logging.error('返回失败')
            if self.name == '完成':
                time.sleep(3)
        else:
            print '测试用例没有执行动作或未识别执行动作'
            raise ValueError('测试用例没有执行动作或未识别执行动作')
        logging.info('结束' + self.action + '动作')

        # 如果预期结果为空，不进行判断操作
        if self.expected == '':
            self.log(actual_value=u'预期页面显示正常', results_value='pass')
            # self.insert_img(self.case_name + '.jpg')
            logging.info('==========测试用执行完成' + self.case_id + '===========\n\r')
        else:
            self.compare_result()

    #失败重试1次
    # @retry(wait_fixed = 2000,stop_max_attempt_number = 2)
    def compare_result(self):
        expectedlist = self.get_expected(self.expected)
        #判断预期页面是字符或者是activity
        if isinstance(expectedlist, list):
            for expected in expectedlist:
                # 查找预期页面元素
                # print expected
                try:
                    self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("' + expected + '")')
                    logging.info('预期页面中存在<' + expected +'>元素')
                    # expect = True
                except BaseException:
                    #比较此时的activity是否和之前的一样，相同说明跳转页面失败
                    if self.before_activity == self.driver.current_activity:
                        raise ValueError('页面跳转失败，再次点击按钮')

                    logging.error('预期页面中不存在<' + expected + '>元素')
                    self.insert_img(self.case_name + '.jpg')
                    self.log(actual_value=u'实际页面中不存在:<' + expected+ '>', results_value='fail')
                    # self.insert_img(self.case_name + '.jpg')
                    logging.info('==========测试用执行完成' + self.case_id + '===========\n\r')
                    msg = '预期界面中不存在<' + expected + '>元素'
                    assert False, msg
        else:
            if self.driver.current_activity == expectedlist:
                logging.info('预期界面中存在<'+expectedlist+'>activity')
            else:
                logging.error('预期界面中不存在<'+expectedlist+'>activity')
                self.insert_img(self.case_name + '.jpg')
                self.log(actual_value=u'预期页面元素显示不正常', results_value='fail')
                logging.info('==========测试用执行完成' + self.case_id + '===========\n\r')
                msg = '预期界面中不存在<'+expected+'>activity'
                assert False,msg

        #self.insert_img(self.case_name + '.jpg')
        self.log(actual_value=u'预期页面显示正常', results_value='pass')
        logging.info('==========测试用执行完成' + self.case_id + '===========\n\r')

if __name__ == '__main__':
    p = Testcase()