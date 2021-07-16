# -*- coding: utf-8 -*-
# @Time     : 2021/7/2 3:06 下午
# @Author   : LiuShiWen

import zmail
import traceback
import openpyxl
from Common.getLog import logger
from Common.getConfig import getEmailOptionValues

class SendEmail(object):
    def __init__(self, subject, content_text=None, content_html_file=None, attachments=None):
        '''
        构造方法，初始化邮件内容
        :param subject: type:string;主题
        :param content_text: type:string,自定义文本
        :param content_html_file: type:string; html file path;
        :param attachments: type:list;附件
        '''
        self.subject = subject
        self.content_text = content_text
        self.content_html_file = content_html_file
        self.attachments = attachments
        self.msg = None
        self.logger = logger('error')
        self.username = getEmailOptionValues()[0]
        self.password = getEmailOptionValues()[1]

    def mail_message(self):
        '''邮件信息'''
        if self.content_text:
            if self.attachments:
                if isinstance(self.attachments, list):
                    try:
                        self.msg = {
                            'subject': '主题' + self.subject,
                            'content_text': self.content_text,
                            'attachments': self.attachments
                        }
                        return self.msg
                    except BaseException as e:
                        self.logger.error(traceback.format_exc())
                else:
                    self.logger.error("附件类型不是list")
            else:
                self.msg = {
                    'subject': '主题' + self.subject,
                    'content_text': self.content_text
                }
                return self.msg
        elif self.content_html_file:
            try:
                with open(file=self.content_html_file, mode="r", encoding="utf-8") as file:
                    self.content_html = file.read()
            except BaseException as e:
                self.logger.error(traceback.format_exc())
            if self.attachments:
                if isinstance(self.attachments, list):
                    try:
                        self.msg = {
                            'subject': '主题' + self.subject,
                            'content_html': self.content_html,
                            'attachments': self.attachments
                        }
                        return self.msg
                    except BaseException as e:
                        self.logger.error(traceback.format_exc())
                else:
                    self.logger.error("附件类型不是list")
            else:
                self.msg = {
                    'subject': '主题' + self.subject,
                    'content': self.content_html
                }
                return self.msg
        else:
            self.logger.info("未传入邮件内容或邮件内容格")

    def send_email(self,recipients_info=None,carbon_copy_info = None,username = '516001590@qq.com',password = 'ubonxsjozawobija'):
        '''
        邮件发送
        :param recipients_info: 接收人;type:list
        :param carbon_copy_info: 抄送人;type:list
        :param username: 用户名
        :param password: 授权码
        :return:
        '''
        try:
            if recipients_info and isinstance(recipients_info,list):
                self.server = zmail.server(username,password)
                if carbon_copy_info and isinstance(carbon_copy_info,list):
                    self.server.send_mail(recipients=recipients_info,cc=carbon_copy_info,mail=self.msg)
                else:
                    self.server.send_mail(recipients=recipients_info,mail=self.msg)
            else:
                self.logger.info('无收件人信息或者格式错误，需要传入list或string格式')
        except:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info('邮件发送成功')

if __name__ == '__main__':
    text = "这是一条测试邮件"
    file = r'2020-05-20-23_11_43_result.html'
    attach = [r'2020-05-20-23_11_43_result.html']
    recipients_info = ['1599932996@qq.com','liushiwen@bolean.com.cn']
    carbon_copy_info = ['516001590@qq.com']
    # send = SendEmail(subject='邮件封装',content_text=text,attachments=attach)
    send = SendEmail(subject='邮件封装',content_html_file=file, attachments=attach)
    send.mail_message()
    send.send_email(recipients_info=recipients_info,carbon_copy_info=carbon_copy_info)
