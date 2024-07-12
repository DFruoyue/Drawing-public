from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import json
from .configerror import ConfigError
from .Activity import *

class Email(object):
    __smtp_server:str = None
    __smtp_port:int = None
    __sender_address:str = None
    __sender_password:str = None

    #初始化
    def __init__(self, email_config_file:str) -> None:
        self.__load_email_config(email_config_file)

    #私有方法
    #检查登录
    def __check_login(self)->bool:
        try:
            server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
            server.starttls()
            server.login(self.__sender_address, self.__sender_password)
            server.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            return False

    #加载邮箱配置
    def __load_email_config(self, email_config_file: str) -> None:
        try:
            with open(email_config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                self.__smtp_server = config_data.get('smtp_server', None)
                self.__smtp_port = config_data.get('smtp_port', None)
                self.__sender_address = config_data.get('sender_address', None)
                self.__sender_password = config_data.get('sender_password', None)
                if self.__smtp_server == None:
                    raise ConfigError('SMTP服务器地址smtp_server未配置')
                if self.__smtp_port == None:
                    raise ConfigError('SMTP服务器端口smtp_port未配置')
                if self.__sender_address == None:
                    raise ConfigError('发件人地址sender_address未配置')
                if self.__sender_password == None:
                    raise ConfigError('发件人密码sender_password未配置')
                if not self.__check_login():
                    raise ConfigError('发件人登录失败')
        except ConfigError as e:
            print(e)
            sys.exit()
        except FileNotFoundError:
            print(f"----------邮箱设置文件错误,错误信息:[未找到'{email_config_file}'文件]----------")
            sys.exit()
        except json.JSONDecodeError:
            print(f"----------邮箱设置文件错误,错误信息:['{email_config_file}'文件内容违反Json规则]----------")
            sys.exit()
        except Exception as e:
            print(f"----------邮箱设置文件错误,错误信息:[未预测到的错误:{e}]----------")
            sys.exit()

    #发送邮件
    def __send_email(self, receiver:Applicant, activity_time:str, chargeLink:str, time_limit:str)->str:
        # 创建邮件内容
        message = MIMEMultipart()
        message['From'] = self.__sender_address
        message['To'] = receiver._email_address
        message['Subject'] = activity_time+'下厨房活动通知'
        
        # 邮件正文内容
        mail_content = '''<!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>HTML Editor - LDDGO.NET</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css" type="text/css">
        </head>
        <body>

        <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">亲爱的'''+receiver._name+'''同学，你好！</span></span></div>
        <div>&nbsp;</div>
        <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 恭喜你抽中本次下厨房活动！</span></span></div>
        <div>&nbsp;</div>
        <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 扫码或者点开问卷链接，填写你的名字，扫码缴费并提交截图提交后问卷会<strong>弹出活动群二维码</strong>，请扫码进群。</span><span style="color: #000000;">注意：</span>若<strong>【'''+time_limit+'''】</strong>前未完成操作，视为<strong>&nbsp;<span style="color: #ff1f00;">放弃名额&nbsp;</span></strong><span style="color: #000000;">！</span></span></div>
        <div>&nbsp;</div>
        <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 如有疑问和其它特殊情况，请添加活动群中的 &ldquo;胡椒蛮馋&rdquo;（肖子奡）或 &ldquo;dreamer&rdquo;（陈可人）。</span></span></div>
        <div>&nbsp;</div>
        <div><span style="color: #000000; font-family: 'times new roman', times, serif; font-size: 14pt;">附缴费问卷链接：'''+chargeLink+'''</span></div>

        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js" type="text/javascript"></script>
        <script type="text/javascript">hljs.highlightAll();</script>
        </body>
        </html>'''
        
        # 添加邮件正文
        message.attach(MIMEText(mail_content, 'html', 'utf-8'))

        try:
            # 连接到SMTP服务器
            session = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
            session.starttls() # 启动TLS加密
            session.login(self.__sender_address, self.__sender_password) # 登录到SMTP服务器
            text = message.as_string()
            session.sendmail(self.__sender_address, receiver._email_address, text)
            session.quit()
            return '√'
        except Exception as e:
            print(f"{receiver._email_address}邮件发送失败:{e}")
            return '✕!!!'
        
    def send(self, activity:Activity, test:bool = True) -> None:
        if test:
            for lucky_dog in activity.lucky_dogs:
                lucky_dog._result = '测试'
            print('测试模式,不发送邮件')
        else:
            for lucky_dog in activity.lucky_dogs:
                lucky_dog._result = self.__send_email(lucky_dog, activity._activity_time, activity._chargeLink, activity._timeLimit)
            print('邮件发送完成')