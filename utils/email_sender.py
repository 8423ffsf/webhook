import smtplib
from email.mime.text import MIMEText
from config.settings import WebhookConfig

def send_html_email(subject, content):
    """
    HTML邮件发送工具
    参数：
        subject: 邮件主题
        content: HTML格式内容
    """
    cfg = WebhookConfig.SMTP_CONFIG
    
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = cfg['sender']
    msg['To'] = cfg['receiver']

    try:
        with smtplib.SMTP_SSL(cfg['server'], cfg['port']) as server:
            server.login(cfg['user'], cfg['password'])
            server.sendmail(cfg['sender'], [cfg['receiver']], msg.as_string())
    except Exception as e:
        raise RuntimeError(f"邮件发送失败: {str(e)}")