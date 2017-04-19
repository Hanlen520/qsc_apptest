# __author__ = 'zzy'
#-*-coding:utf-8-*-
from lxml import etree
from xlutils.copy import copy
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
# from PIL import Image
from fractions import Fraction
import sys,os,time
import xlrd
import logging
import math
import operator
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
'''
============说明================
功能:页面基础类,包含所有页面公用的函数
================================
'''

class Page(object):
    '''
    页面基础类，用于所有页面的继承
    '''
    def __init__(self,appium_driver = None,parent =None):

        self.driver = appium_driver
        self.timeout = 30
        self.parent = parent
        self.path = os.path.dirname(__file__)
        self.log_txt = self.path.split('test_case')[0] + 'data/log.txt'   #配置日志文件位置
        self.f_xml = self.path.split('test_case')[0] + 'data/element.xml' #配置xml文件位置
        # self.f_xls = self.path.split('test_case')[0] + 'data/TestCase.xls'#配置xls文件位置
        self.img_expected = self.path.split('test_case')[0] + 'data/image/'#配置预期截图文件位置
        self.img_actual = self.path.split('test_case')[0] + 'report/image/'  #配置实际截图文件位置
        self.img_path = self.path.split('test_case')[0] + 'report/image/image.txt'#配置上传图片路径
        self.open_xml = etree.parse(self.f_xml)                             #将xml解析为树结构
        # self.open_xls = xlrd.open_workbook(self.f_xls, formatting_info=True)#打开xls文件
        self.host = '172.16.10.83'
        self.database = 'myweb'
        self.username = 'root'
        self.password = '12345678'

        # # 定义log日志文件类型\格式\级别test
        # self.logger = logging.getLogger('zzy')
        logging.basicConfig(level=logging.INFO ,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.log_txt,
                            filemode='w')

        # console = logging.StreamHandler()
        # console.setLevel(logging.INFO)
        # # 设置日志打印格式
        # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # console.setFormatter(formatter)
        # # 将定义好的console日志handler添加到root logger
        # # self.logger.addHandler(console)
        # logging.getLogger('zzy').addHandler(console)
        # logging._removeHandlerRef(console)

    # 打开activity
    def start_appActivity(self,app_package,app_activity):
        self.driver.start_activity(app_package,app_activity)
        assert self.on_page(),'Did not land on %s' % self.app_activity

    # 查找单个元素
    def find_element(self,*loc):
        return self.driver.find_element(*loc)

    # 查找一组元素函数
    def find_elements(self,*loc):
        return self.driver.find_elements(*loc)

    def get_element(self,elementdict):
        logging.info('开始定位元素')
        try:
            if elementdict['pathtype'] == 'id':
                if 'index' in elementdict:
                    element = self.find_elements(By.ID,elementdict['pathvalue'])
                    # for i in element:
                    #     print i
                    if element:
                        logging.info('id定位成功')
                        return element[int(elementdict['index'])]
                    else:
                        logging.error('id定位失败')
                        return None
                else:
                    element = self.find_element(By.ID,elementdict['pathvalue'])
                    # print element
                    if element:
                        logging.info('id定位成功')
                        return element
                    else:
                        logging.error('id定位失败')
                        return None

            if elementdict['pathtype'] == 'name':
                # element = self.find_By.NAME, elementdict['pathvalue'])
                element = self.driver.find_element_by_android_uiautomator('new UiSelector().text("' + elementdict['pathvalue'] + '")')
                if element:
                    logging.info('name定位成功')
                    return element
                else:
                    logging.error('name定位失败')
                    return None

            if elementdict['pathtype'] == 'class':
                if 'index' in elementdict:
                    element = self.find_elements(By.CLASS_NAME, elementdict['pathvalue'])[int(elementdict['index'])]
                    if element:
                        logging.info('class定位成功')
                        return element
                    else:
                        logging.error('class定位失败')
                        return None
                else:
                    element = self.find_element(By.CLASS_NAME, elementdict['pathvalue'])
                    if element:
                        logging.info('class定位成功')
                        return element
                    else:
                        logging.error('class定位失败')
                        return None
            if elementdict['pathtype'] == 'coordinate':
                    logging.info('coordinate定位成功')
                    return elementdict

        except Exception,e:
            logging.error('元素定位失败')
            print e
            return None

    # 判断activity函数
    def on_page(self):
        return (self.driver.current_activity) == (self.app_activity)

    # 执行脚本函数
    def script(self,src):

        return self.driver.execute_script(src)
    def my_tag(self,x,y,duration):
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
        except BaseException,e:
            print e
            return False

    def my_swipe2(self,start_x, start_y, end_x, end_y, duration=200):
        time.sleep(3)
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            return True
        except BaseException,e:
            print e
            return False

    def my_swipe(self,direction,value,during=200):
        """
        swipe UP
        :param during:
        :return:
        """
        time.sleep(3)
        window_size = self.driver.get_window_size()
        # window_size = get_window_size()
        width = window_size.get("width")
        height = window_size.get("height")
        if direction == 'down':
            i = Fraction(1) - Fraction(value)
            try:
                self.driver.swipe(width / 2, height * 3 / 4, width / 2, height * i.numerator / i.denominator, during)
                return True
            except Exception,e:
                print e
                return False
        elif direction == 'up':
            i = Fraction(value)
            try:
                self.driver.swipe(width / 2, height / 4 , width / 2, height * i.numerator / i.denominator, during)
                return True
            except Exception, e:
                print e
                return False
        elif direction == 'right':
            i = Fraction(1,4) + Fraction(value)
            try:
                self.driver.swipe(width / 4, height / 2, width * i.numerator / i.denominator , height / 2, during)
                return True
            except Exception, e:
                print e
                return False
        elif direction == 'left':
            i = (Fraction(3,4) - Fraction(value))
            try:
                self.driver.swipe(width * 3 / 4, height / 2, width * i.numerator / i.denominator, height / 2, during)
                return True
            except Exception, e:
                print e
                return False
        else:
            return False

    # 截图函数
    def insert_img(self,file_name):
        # base_dir = os.path.dirname(os.path.dirname(__file__))
        # base_dir = str(base_dir)
        # base_dir = base_dir.replace('\\', '/')
        # base = base_dir.split('test_case')[0]
        # file_path = base + "report/image/" + file_name
        file_path = self.img_actual + file_name
        try:
            self.driver.get_screenshot_as_file(file_path)
            with open(self.img_path, 'a') as f:
                f.write(file_path + '\n')
                logging.info(u'写入图片路径成功:')
            logging.info(u'获取截图成功:')
            logging.info(u'截图保存至:' + file_path)
        except:
            logging.error(u'获取截图失败:')

    # 图片对比函数
    def similarity_image(self,file_name1, file_name2,standard = 1):

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

        # im1 = '/Users/zzy/Pictures/110913085047472.gif'
        # im2 = '/Users/zzy/Pictures/110913085047471.gif'

    #获取mysq数据库中的测试用例
    def get_mysql(self, table):
        #连接数据库
        conn = MySQLdb.connect(host=self.host, user=self.username,
                               passwd=self.password, db=self.database, port=3306)
        conn.set_character_set('utf8')
        with conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            sql = '''select * from %s''' % table
            cur.execute(sql)
            testcases_list = cur.fetchall()
            return testcases_list

    # 获取xml文件中元素的定位信息,返回元素字典
    def get_xml(self, activity_name, element_name):
        # print type(activity_name),type(element_name)
        #将xml解析为树结构
        # tree = etree.parse(self.f_xml)
        #获得该树的树根
        root = self.open_xml.getroot()
        elementdict = {}
        try:
            for activity_parents in root:
                # 遍历所树种的activity父节点
                # if isinstance(activity_parents.get('name'), str):
                #     print activity_parents.get('name')
                if activity_parents.get('name') == activity_name:
                    # print activity_name
                    # print activity_parents.tag,activity_parents.text
                    for element_parent in activity_parents:
                        # 遍历主父节点中的element子节点
                        if element_parent.get('name') == element_name:
                            # print element_name
                            # print element_parent.tag,element_parent.get('name')
                            # print '查找到父节点'
                            for element_child in element_parent:
                                # 获取element子节点中的value
                                if isinstance(element_child.tag, str):
                                    # print element_child.tag,":",element_child.text
                                    # 将获取的value添加至elementdict字典中
                                    elementdict[element_child.tag] = element_child.text
                            logging.info('获取activity:'+ activity_name + ',element_name:' + element_name + ',元素信息:')
                            logging.info(elementdict)
                            return elementdict
                            # return self.get_element(elementdict)
                        # else:
                        #     logging.error('获取activity子节点失败!')
                        #     return None
                # else:
            logging.error('未找到activity信息!')
            return None
        except:
            logging.error('获取activity失败!')
    # 获取xls文件中的测试用例集,返回字典形式的测试用例集合

    def get_xls(self, sheet_name):
        #获取xls sheet页
        table = self.open_xls.sheet_by_name(sheet_name)
        nrows = table.nrows  # 获取行数
        ncols = table.ncols  # 获取列数
        #定义测试用例集列表
        testcases_list = []
        try:
            for row in range(nrows):
                #定义单个测试用例字典
                testcase_dict = {}
                if row: #首行标题不添加字典中
                    for col in range(ncols):
                        testcase_dict[table.cell(0, col).value] = table.cell(row, col).value
                    testcases_list.append(testcase_dict)
            # for testcase_dict in testcases_list:
            #     print '====' * 10
            #     for item, value in testcase_dict.items():
            #         print 'key=%s, value=%s' % (item, value)
            logging.info('获取测试用例')
            return testcases_list
        except:
            logging.error('未获取测试用例')
            raise error('测试用例获取失败')

    # 获取excel表格中sheet对应的index
    def get_sheet_index(self, sheet_name):
        #输入sheet页,返回index
        sheets = self.open_xls.sheet_names()
        for index, item in enumerate(sheets):
            if item == sheet_name:
                # print index, item
                return index

    # 获取excel表格中单元格坐标,返回字典坐标
    def get_cell(self,sheet_name,case_id):
        cell_dict = {}
        table = self.open_xls.sheet_by_name(sheet_name)
        # nrows = table.nrows  # 获取行数
        # ncols = table.ncols  # 获取列数
        #   # 获取整行（数组）
        # table.col_values(i)  # 整列的值（数组）
        for index,item in enumerate(table.col_values(0)):
            if item == case_id:
                cell_dict['row'] = index
                break
        for index,item in enumerate(table.row_values(0)):
            if item == 'results':
                cell_dict['col'] = index
                break
        return cell_dict

    # 写入excel表格中result结果
    def set_xls(self,sheet_index,row, col, value):

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
        except:
            return False

    # 将测试结果写入excel表格中
    def results(self,sheet_name,case_id,col,value):
        #获取sheet_index
        sheet_index = self.get_sheet_index(sheet_name)
        #获取results单元格坐标
        cell = self.get_cell(sheet_name,case_id)

        if col == 'results':
            row = cell['row']
            col = cell['col']
        if col == 'actual':
            row = cell['row']
            col = int(cell['col']) - 1

        # 结果写入excel
        if self.set_xls(sheet_index,row,col,value):
            # logging.info('测试结果写入成功!')
            return True
        else:
            # logging.error('测试结果写入失败!')
            return False

    def set_mysql(self,table,case_id,col,value):
        # 连接数据库
        conn = MySQLdb.connect(host=self.host, user=self.username,
                               passwd=self.password, db=self.database, port=3306)
        conn.set_character_set('utf8')
        with conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            if col == 'results':
                sql = '''UPDATE %s SET result = '%s' WHERE case_id = '%s';''' %(table,value,case_id)
            if col == 'actual':
                sql = '''UPDATE %s SET actual = '%s' WHERE case_id = '%s';''' %(table,value,case_id)
            try:
                cur.execute(sql)
                return True
            except BaseException,e:
                print e
                return False


if __name__ == '__main__':
    p = Page()
    # print p.f_img
    # print p.get_xml('MainActivity',u'尝鲜预售')
    # case = p.get_mysql('a_login')
    # for i in case:
    #     print i
    # p.get_xls('login')
    # index = p.get_sheet_index('add_cart')
    # p.set_xls(index,1,6,'fail')
    # try:
    #     cell = p.results('login','qsc_login_03',u'失败')
    # except:
    #     print u'写入结果失败'
    # logging.info('写入结果失败')
    t = p.set_mysql('a_login','test1_Login_06','actual','yes')
    print t