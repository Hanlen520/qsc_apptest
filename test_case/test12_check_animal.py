# __author__ = 'zhanghzhiyuan'
# -*-coding:utf-8-*-

from models import myunit
from models.base import Page
from models.buildcase import Testcase
import unittest

'''
===========说明============
功能:测试用例定义
入口:ecxel表格测试用例
==========================
'''

class Androidtest(myunit.MyTest):
    '''轻松筹:微爱动物保护项目管理'''
    Page = Page()

    FUNC_TEMPLATE = '''@unittest.skipUnless({state},'state值为0,跳过测试')\ndef {func}(self):
           '{casename}'
           Testcase(self.driver,{onecase},'{sheetname}').execute_case()
           '''

    # 获取sheet页中state状态为1(可执行)的测试用例,返回测试用例字典
    testcaselist = Page.get_mysql('a_check_love')
    for testcase in testcaselist:
        # 判断测试用例是否执行 1——执行,0——不执行;
        exec (FUNC_TEMPLATE.format(func=testcase['case_id'],
                                   casename=testcase['case_name'],
                                   onecase=testcase,
                                   sheetname='a_check_love',
                                   state=testcase['state'] in [1,2]
                                   ))
    # def __del__(self):
    #     if __name__ != '__main__':
    #         return self


if __name__ == '__main__':
    unittest.main()