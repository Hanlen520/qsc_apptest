#-*-coding:utf-8-*-
'''
-----------------------------------------------
功能：
将Django平台的自动化测试用转化为MQC平台上可执行测试用例
-----------------------------------------------
'''
import os
import sys
import time
from qscapp.test_case.models.base import Page
reload(sys)
sys.setdefaultencoding('utf-8')


class Conversion_mqc(Page):

	def __init__(self,table):
		super(Conversion_mqc, self).__init__()
		self.now = time.strftime("%m-%d_%H:%M")
		self.steps = ''
		self.step = ''
		self.table = table

	def get_testcase(self):
		testcaselist = self.get_mysql(self.table)
		for testcase in testcaselist:
			# print testcase
			step = []
			if testcase['action'] == 'click':
				# step.append('click')
				# step.append(\n)
				if testcase['activity']:
					elementdict = self.get_xml(testcase['activity'],testcase['name'])
					# print elementdict
					if elementdict['pathtype'] == 'id':
						if 'index' in elementdict:
							self.step = "['click',None,'%s',None,None,None,%s]" %(elementdict['pathvalue'],elementdict['index'])
						else:
							self.step = "['click',None,'%s',None,None,None,None]" %(elementdict['pathvalue'])
				else:
					self.step = "['click',None,None,'%s',None,None,None]" %(testcase['name'])

			if testcase['action'] == 'tag':
				point = eval(testcase['value'])
				if len(point) > 2:
					self.step = "['longclick',None,None,None,%s,%s,None,%s]" %(point[0],point[1],point[2])
				else:
					self.step = "['click',None,None,None,%s,%s,None,None]" %(point[0],point[1])
			if testcase['action'] == 'sendkey':
				if testcase['activity']:
					elementdict = self.get_xml(testcase['activity'],testcase['name'])
					if elementdict['pathtype'] == 'id':
						if 'index' in elementdict:
							self.step = "['send_text',None,'%s','%s',%s,None]" %(elementdict['pathvalue'],testcase['value'],elementdict['index'])
						else:
							self.step = "['send_text',None,'%s','%s',None]" %(elementdict['pathvalue'],testcase['value'])
				else:
					self.step = "['send_text',None,None,'%s',None,'%s']" %(testcase['value'],testcase['name'])

			if testcase['action'] == 'swipe':
				if testcase['activity']:
					elementdict = self.get_xml(testcase['activity'],testcase['name'])
					self.step = "['swipe',[(%s,%s),(%s,%s)],None]" %(elementdict['start_x'],elementdict['start_y'],elementdict['end_x'],elementdict['end_y'])
				else:
					self.step = "['swipe',None,'%s']" %(testcase['value'].split(',')[0])

			if testcase['action'] == 'sleep':
				self.step = "['sleep',%s]" %(testcase['value'])

			if testcase['action'] == 'back':
				self.step = "['keycode', [(4, None)]]"

			tab = ' ' * 16
			self.step = '\n' + tab + '# ' + testcase['case_id'] + ' ' + testcase['case_name'] + '\n' + tab + self.step + ','
			self.steps = self.steps + self.step
		return self.steps

	def create_file(self,steps):

		with open('mqc_demo.py') as f:
			# s = f.readlines()
			# for i in s:
			# 	print i
			ALL = f.xreadlines()
			with open('main.py','wb') as f_new:
				for i in ALL:
					i = i.replace("'测试用例'",steps)
					f_new.write(i)

if __name__ == '__main__':
	C = Conversion_mqc('a_dream_project_released') #输入要转化的测试用例表
	steps = C.get_testcase()
	C.create_file(steps)