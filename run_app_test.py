# __author__ = 'zhagnzhiyuan'
#-*-coding:utf-8-*-
import sys
sys.path.append('./package')
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import mimetypes
import smtplib
import unittest
import time
import os
import ConfigParser
'''
==============说明===============
功能:测试用例执行,html报告生成,邮件发送
入口:测试用例目录
================================
'''
reload(sys)
sys.setdefaultencoding('utf8')
# =========================邮件接收者============================
mailto_list = sys.argv[3:] #接收命令行传入参数
#============= 设置服务器，用户名、口令以及邮箱的后缀===============
mail_host="smtp.exmail.qq.com"
mail_port="465"
mail_user="********"
mail_pass="********"
#===========================发送邮件============================
def send_mail(to_list,file_new,attach_list):
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    me=mail_user
    text = MIMEText(mail_body,'html','utf-8')
    msg = MIMEMultipart()
    msg.attach(text)

    # 构造MIMEImage对象做为文件附件内容并附加到根容器
    for file_name in attach_list:
        ctype, encoding = mimetypes.guess_type(file_name)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        file_msg = MIMEImage(open(file_name, 'rb').read(), subtype)

        ## 设置附件头
        basename = os.path.basename(file_name)
        file_msg.add_header('Content-Disposition', 'attachment', filename=basename.decode('utf8').encode('gb2312'))  # 修改邮件头
        msg.attach(file_msg)

    msg['Subject'] = u'轻松筹Android自动化测试报告'
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP_SSL(mail_host, mail_port)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

#==============查找测试报告目录，找到最新生成的测试报告文件==========
def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn:os.path.getatime(testreport + "//" + fn))
    file_new = os.path.join(testreport,lists[-1])
    # print(file_new)
    return file_new

if __name__ == '__main__':
    #获取config.ini文件位置
    f_ini  = os.path.dirname(__file__) + 'qscapp/data/config.ini'
    #实例化配置文件
    config = ConfigParser.ConfigParser()
    config.read(f_ini)
    #获取设备名称
    name = sys.argv[2]
    #写入config.ini文件中
    config.set('APPCONFIG','name',unicode(name))
    with open(f_ini,"w+") as f:
        config.write(f)

    parameter = sys.argv[1] #接受命令行传入参数
    testcase = parameter + '.py'
    # print testcase
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './qscapp/report/html/' + now +'.html'
    # filename = './qscapp/report/html/11.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner(stream=fp,
                            title=u'轻松筹Android自动化测试报告',
                          description=u'环境 ：Android 版本：5.1.1')
    discover = unittest.defaultTestLoader.discover('./qscapp/test_case',
                                                   pattern=testcase)
    # suite = unittest.TestSuite
    # suite.addTest()

    runner.run(discover)
    fp.close()
    file_path = new_report('./qscapp/report/html/')
    image_list = []
    with open('./qscapp/report/image/image.txt','r+') as f:
        for each in f.readlines():
            image_list.append(each.split('\n')[0])
        f.seek(0)
        f.truncate()
    # print image_list
    temp = open(file_path, 'rb')
    a = temp.read()  # 读取报告内容
    temp.close()
    p = r"<td class='errorCase'>"  #查找报告中错误内容
    q = r"<td class='failCase'>"
    if p in a or q in a:
        print('we need to send E-mail.')
        if send_mail(mailto_list, file_path,image_list):
            print u"发送成功"
        else:
            print u"发送失败"
    else:
        print(u'测试通过不发送报告')