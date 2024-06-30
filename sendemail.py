from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configerror as cfg
from activityinformation import ActivityInformation
from member import Member
import sys
class EmailConfig(object):
    def __init__(self, sender_address = None, sender_password = None, smtp_server = None, smtp_port = None):
        self.sender_address = sender_address
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    def __init__(self):
        try:
            with open('email.cfg', 'r', encoding='utf-8') as emailconfigfile:
                emailconfig = {}
                lines = emailconfigfile.read().splitlines()
                for line in lines:
                    if ':' in line:
                        key,value = line.split(':',1)
                        emailconfig[key] = value
                if 'smtp_server' in emailconfig:
                    self.smtp_server = emailconfig['smtp_server']
                else:
                    raise cfg.ConfigError('smtp_server',5)
                if 'smtp_port' in emailconfig:
                    self.smtp_port = int(emailconfig['smtp_port'])
                else:
                    raise cfg.ConfigError('smtp_pert未配置',6)
                if 'sender_address' in emailconfig:
                    self.sender_address = emailconfig['sender_address']
                else:
                    raise cfg.ConfigError('sender_addres未配置',7)
                if 'sender_password' in emailconfig:
                    self.sender_password = emailconfig['sender_password']
                else:
                    raise cfg.ConfigError('sender_password未配置',8)
        except cfg.ConfigError as e:
            print(e)
            sys.exit()
        except:
            print('\'email.cfg\'文件打开失败')
            sys.exit()
    def check_login(self)->bool:
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_address, self.sender_password)
            server.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            return False

def send_email(receiver:Member, sender_email_config:EmailConfig, activity_information:ActivityInformation)->str:
    # 创建邮件内容
    message = MIMEMultipart()
    message['From'] = sender_email_config.sender_addres
    message['To'] = receiver.email_address
    message['Subject'] = activity_information.activity_time+'下厨房活动通知'
    
    # 邮件正文内容
    mail_content = '''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>HTML Editor - LDDGO.NET</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/styles/default.min.css" type="text/css">
    </head>
    <body>

    <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">亲爱的'''+receiver.name+'''同学，你好！</span></span></div>
    <div>&nbsp;</div>
    <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 恭喜你抽中本次下厨房活动！</span></span></div>
    <div>&nbsp;</div>
    <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 扫码或者点开问卷链接，填写你的名字，扫码缴费并提交截图提交后问卷会<strong>弹出活动群二维码</strong>，请扫码进群。</span><span style="color: #000000;">注意：</span>若<strong>【'''+activity_information.timelimit+'''】</strong>前未完成操作，视为<strong>&nbsp;<span style="color: #ff1f00;">放弃名额&nbsp;</span></strong><span style="color: #000000;">！</span></span></div>
    <div>&nbsp;</div>
    <div><span style="font-family: 'times new roman', times, serif; font-size: 14pt;"><span style="color: #000000;">&nbsp; &nbsp; &nbsp; &nbsp; 如有疑问和其它特殊情况，请添加活动群中的 &ldquo;胡椒蛮馋&rdquo;（肖子奡）或 &ldquo;dreamer&rdquo;（陈可人）。</span></span></div>
    <div>&nbsp;</div>
    <div><span style="color: #000000; font-family: 'times new roman', times, serif; font-size: 14pt;">附缴费问卷链接：'''+activity_information.chargelink+'''</span></div>

    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/highlight.min.js" type="text/javascript"></script>
    <script type="text/javascript">hljs.highlightAll();</script>
    </body>
    </html>'''
    
    # 添加邮件正文
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))

    try:
        # 连接到SMTP服务器
        session = smtplib.SMTP(sender_email_config.smtp_server, sender_email_config.smtp_port)
        session.starttls() # 启动TLS加密
        session.login(sender_email_config.sender_address, sender_email_config.sender_password) # 登录到SMTP服务器
        text = message.as_string()
        session.sendmail(sender_email_config.sender_address, receiver.address, text)
        session.quit()
        return '√'
    except Exception as e:
        return '✕!!!'