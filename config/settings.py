import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class WebhookConfig:
    """动态配置管理类"""
    
    # 认证配置
    AUTH_SCHEME = os.getenv("AUTH_SCHEME", "Bearer")
    SECRET_TOKEN = os.getenv("WEBHOOK_TOKEN")
    
    # 字段映射配置
    REQUIRED_FIELDS = os.getenv("REQUIRED_FIELDS", "event_type,data.user_id").split(',')
    
    # 邮件配置
    SMTP_CONFIG = {
        'server': os.getenv("SMTP_SERVER"),
        'port': int(os.getenv("SMTP_PORT", 465)),
        'user': os.getenv("SMTP_USER"),
        'password': os.getenv("SMTP_PASSWORD"),
        'sender': os.getenv("EMAIL_FROM"),
        'receiver': os.getenv("EMAIL_TO")
    }
    
    # 模板配置
    TEMPLATE_SETTINGS = {
        'auto_reload': os.getenv("TEMPLATE_AUTO_RELOAD", True),
        'cache_size': int(os.getenv("TEMPLATE_CACHE_SIZE", 400))
    }