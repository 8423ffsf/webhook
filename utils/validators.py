from config.settings import WebhookConfig

def validate_request(auth_header):
    """验证请求头有效性"""
    if not auth_header:
        return False
    try:
        scheme, token = auth_header.split()
        return scheme == WebhookConfig.AUTH_SCHEME and token == WebhookConfig.SECRET_TOKEN
    except ValueError:
        return False