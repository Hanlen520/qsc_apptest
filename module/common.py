# -*- coding:utf-8 -*-
import xlrd
import logging
import math
import operator
from logging.config import fileConfig
from xlutils.copy import copy
import xml.etree.ElementTree as etree
from PIL import Image
from qsc_apptest.config.configure import Config
import pymysql
import sqlite3
import sys

class Common(object):

    def __init__(self):

        config = Config()
        self.log_txt = config.log_path
        self.f_xml = config.xml_path
        self.f_xls = config.xls_path
        self.img_expected = config.img_expected_path
        self.img_actual = config.img_actual_path
        self.img_path = config.img_path
        self.db_type = config.db_type
        self.host = config.db_host
        self.database = config.db_database
        self.username = config.db_name
        self.password = config.db_pass
        self.port = config.db_port
        self.config_path = config.config_path

    def __dbConn(self):
        """
        :return: db_conn
        """
        if self.db_type != "mysql" and self.db_type != "sqlite3":
            logger.error("数据库类型错误：'mysql' or 'sqlite3'")
            raise ConnectionAbortedError("数据库类型错误")
        if self.db_type == "mysql":
            conn = pymysql.connect(host=self.host, user=self.username,
                               passwd=self.password, db=self.database, port=int(self.port))
            # conn.set_character_set('utf8')
        if self.db_type == "sqlite3":
            conn = sqlite3.connect(self.database)

        return conn

    def __xlsConn(self):
        """
        :return: xls_conn
        """
        conn = xlrd.open_workbook(self.f_xls, formatting_info=True)
        return conn

    def __xmlConn(self):
        """
        :return: xml_conn
        """
        conn = etree.parse(self.f_xml)
        return conn

    def GetXls(self, sheet_name):
        """
        :param sheet_name:
        :return: 测试用例集
        """

        #获取xls sheet页
        table = self.__xlsConn().sheet_by_name(sheet_name)
        nRows = table.nrows  # 获取行数
        nCols = table.ncols  # 获取列数
        #定义测试用例集列表
        testCasesList = []
        try:
            for row in range(nRows):
                #定义单个测试用例字典
                testCaseDict = {}
                if row: #首行标题不添加字典中
                    for col in range(nCols):
                        testCaseDict[table.cell(0, col).value] = table.cell(row, col).value
                    testCasesList.append(testCaseDict)
            # for testcase_dict in testcases_list:
            #     print '====' * 10
            #     for item, value in testcase_dict.items():
            #         print 'key=%s, value=%s' % (item, value)
            logger.info('获取测试用例')
            return testCasesList
        except:
            logger.error('未获取测试用例')
            raise IOError('测试用例获取失败')

    def getXlsSheetIndex(self, sheet_name):
        """
        :param sheet_name:
        :return: excel表格中sheet对应的index
        """
        sheets = self.__xlsConn().sheet_names()
        for index, item in enumerate(sheets):
            if item == sheet_name:
                return index

    def getCell(self,sheet_name,case_id):
        """
        table = self.__xlsConn().sheet_by_name(sheet_name)
        nRows = table.nrows  # 获取行数
        nCols = table.ncols  # 获取列数
        table.row_values(index) # 获取整行（数组）
        table.col_values(index)  # 整列的值（数组）
        :param sheet_name:
        :param case_id:
        :return: 获取excel表格中单元格坐标,返回字典坐标
        """
        cell_dict = {}
        table = self.__xlsConn().sheet_by_name(sheet_name)
        for index,item in enumerate(table.col_values(0)):
            if item == case_id:
                cell_dict['row'] = index
                break
        for index,item in enumerate(table.row_values(0)):
            if item == 'results':
                cell_dict['col'] = index
                break
        return cell_dict

    def setXls(self,sheet_index,row,col,value):

        open_xls = xlrd.open_workbook(self.f_xls, formatting_info=True)  # 打开xls文件
        outwb = copy(open_xls)
        outSheet = outwb.get_sheet(sheet_index)
        try:
            """ Change cell value without changing formatting. """
            def _getOutCell(outSheet, colIndex, rowIndex):
                """ HACK: Extract the internal xlwt cell representation. """
                row = outSheet._Worksheet__rows.get(rowIndex)
                if not row: return None
                cell = row._Row__cells.get(colIndex)
                return cell
            # HACK to retain cell style.
            previousCell = _getOutCell(outSheet, col, row)
            # END HACK, PART I
            outSheet.write(row, col, value)
            # HACK, PART II
            if previousCell:
                newCell = _getOutCell(outSheet, col, row)
                if newCell:
                    newCell.xf_idx = previousCell.xf_idx
                    # END HACK
            outwb.save(self.f_xls)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def SetResults(self,sheet_name,case_id,col,value):
        #获取sheet_index
        sheet_index = self.getXlsSheetIndex(sheet_name)
        #获取results单元格坐标
        cell = self.getCell(sheet_name,case_id)
        row = ''
        if col == 'results':
            row = cell['row']
            col = cell['col']
        if col == 'actual':
            row = cell['row']
            col = int(cell['col']) - 1

        # 结果写入excel
        if self.setXls(sheet_index,row,col,value):
            logger.info('测试结果写入成功!')
            return True
        else:
            logger.error('测试结果写入失败!')
            return False

    def GetXml(self, activity_name, element_name):
        """
        <activity name = ".ui.activity.MainActivity"><!--activity名称-->

            <element name="推荐">
                <name>推荐</name>
                <type>TextView</type>
                <pathType>class</pathType>
                <pathValue>android.widget.TextView</pathValue>
		    	<index>0</index>
            </element>

        </activity>

        :param activity_name:
        :param element_name:
        :return:
        """

        #获得该树的树根
        root = self.__xmlConn().getroot()
        elementDict = {}
        try:
            for activity_parents in root:
                # 遍历所树种的activity父节点
                if activity_parents.get('name') == activity_name:
                    for element_parent in activity_parents:
                        # 遍历主父节点中的element子节点
                        if element_parent.get('name') == element_name:
                            for element_child in element_parent:
                                # 获取element子节点中的value
                                if isinstance(element_child.tag, str):
                                    elementDict[element_child.tag] = element_child.text
                            logger.info('获取activity:'+ activity_name + ',element_name:' + element_name + ',元素信息:')
                            logger.debug(elementDict)
                            return elementDict
                            # return self.get_element(elementdict)
                            # else:
                            #     logging.error('获取activity子节点失败!')
                            #     return None
                            # else:
            logger.error('未找到activity信息!')
            return None
        except Exception as e:
            logger.error('{0}:获取activity失败!'.format(e))

    def GetDevices(self):
        config = Config()
        name = config.name
        conn = self.__dbConn()
        with conn:
            cur = conn.cursor()
            # 通过读取config.ini文件中的设备名称，执行sql命令，从数据库中获取对应设备型号和安卓版本
            sql = 'select deviceName,platformVersion,appiumPort,bootstrapPort,udid,resolution from a_device where name = "{0}"'.format(name)
            print(sql)
        cur.execute(sql)
        #获取设备型号、安卓版本、appium启动端口信息、设备udid
        s = cur.fetchone()
        print(s)
        deviceName = s[0]
        platformVersion = s[1]
        appium_port = s[2]
        bp_port = s[3]
        udid = s[4]
        resolution = s[5]

    def GetTestCaseListForMysql(self, table):
        """
        :param table:
        :return: mysq数据库中的测试用例
        """
        conn = self.__dbConn()
        with conn:
            cur = conn.cursor(pymysql.cursors.DictCursor)
            sql = "select * from %s" % table
            cur.execute(sql)
            testCasesList = cur.fetchall()
            return testCasesList

    def SetTestCaseForMysql(self,table,case_id,col,value):
        # 连接数据库
        conn = self.__dbConn()
        with conn:
            cur = conn.cursor(pymysql.cursors.DictCursor)
            sql = ''
            if col == 'results':
                sql = "UPDATE %s SET result = '%s' WHERE case_id = '%s';" % (table, value, case_id)
            if col == 'actual':
                sql = "UPDATE %s SET actual = '%s' WHERE case_id = '%s';" % (table, value, case_id)
            try:
                cur.execute(sql)
                return True
            except BaseException as e:
                logger.error(e)
                return False

    def get_devices_mysql(self):
        conn = self.__dbConn()
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

    @staticmethod
    def SimilarityImage(file_name1, file_name2, standard = 1):

        image1 = Image.open(file_name1)
        image2 = Image.open(file_name2)
        # image1.show()
        # image2.show()

        h1 = image1.histogram()
        h2 = image2.histogram()
        # print h1,h2
        rms = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        if rms <= standard:
            return True
        else:
            return False

def ExecuteCMD(shell):
    if sys.version_info >= (3,3):
        result = subprocess.check_output(shell)
    else:
        result = commands.getoutput(shell)
    return result

fileConfig(Common().config_path)
logger = logging.getLogger('root')

if __name__ == '__main__':
    c = Common()
    c.GetDevices()
    logger.info("测试")
    logger.warning("这是警告")
    logger.debug("这是调试")
    logger.error("这是错误")
    logger.critical("这是严重")

