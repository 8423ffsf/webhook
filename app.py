"""
Webhook Server Main Module
基于Flask框架的Webhook接收服务，支持Header验证、动态字段解析、HTML邮件通知
"""
from datetime import datetime
from flask import Flask, request, jsonify
from config.settings import WebhookConfig
from utils.email_sender import send_html_email
from utils.validators import validate_request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    处理Webhook请求的核心逻辑
    流程：认证 -> 验证 -> 解析 -> 发送邮件
    """
    try:
        # 1. 身份验证
        auth_header = request.headers.get('Authorization')
        if not validate_request(auth_header):
            return jsonify({"error": "Unauthorized"}), 401

        # 2. 数据验证与解析
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # 3. 动态字段提取
        extracted = {
            field: extract_nested(data, field)
            for field in WebhookConfig.REQUIRED_FIELDS
        }
        if None in extracted.values():
            return jsonify({"error": "Missing required fields"}), 400

        # 4. 生成邮件内容
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_content = app.jinja_env.get_template('report.html').render(
            data=extracted,
            report_time=report_time,
            event_time=datetime.now().isoformat()
        )

        # 5. 发送邮件
        send_html_email(
            subject=f"Webhook Alert - {report_time}", #修改subject的值以改变邮件通知的标题
            content=email_content
        )

        return jsonify({
            "status": "success",
            "received_at": report_time
        }), 200

    except Exception as e:
        app.logger.error(f"处理失败: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def extract_nested(data, field_path):
    """递归提取嵌套字段"""
    keys = field_path.split('.')
    value = data
    for key in keys:
        value = value.get(key, {})
    return value if value != {} else None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)