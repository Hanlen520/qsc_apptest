# __author__ = 'zhanghzhiyuan'
# -*-coding:utf-8-*-
import sys
# sys.path.append(".\models")
# sys.path.append(".\page_obj")
from models import myunit
from models.base import Page
from models.buildcase import Testcase
import unittest
import sys
import logging
'''
===========说明============
功能:测试用例定义
入口:ecxel表格测试用例
==========================
'''


class homePageTest(myunit.MyTest):
    '''首页标切换签页测试'''

    Page = Page()

    # 构建测试用例,一条测试用例对应一个函数
    FUNC_TEMPLATE = '''@unittest.skipUnless({state},'state值为0,跳过测试')\ndef {func}(self):
            '{casename}'
            Testcase(self.driver).execute_case({onecase},'{sheetname}')
            '''
    # 获取sheet页中的测试用例,返回一条测试用例,以字典形式记录测试用例
    testcaselist = Page.get_xls('home')
    for testcase in testcaselist:
        exec (FUNC_TEMPLATE.format(func=testcase['case_id'],
                                   casename=testcase['case_name'],
                                   onecase=testcase,
                                   sheetname='home',
                                   state=testcase['state']
                                   ))

if __name__ == '__main__':
    unittest.main()