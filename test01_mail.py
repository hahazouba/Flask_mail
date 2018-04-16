# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__)


# 配置邮件的第三方服务器的规则：服务器／端口／安全套接字层／邮箱名／授权码
app.config['MAIL_SERVER'] = "smtp.yeah.net"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "dailyfreshzxc@yeah.net"
app.config['MAIL_PASSWORD'] = "dailyfresh123"
app.config['MAIL_DEFAULT_SENDER'] = 'FlaskAdmin<dailyfreshzxc@yeah.net>'

# 创建发送邮件的客户端
mail = Mail(app)


@app.route('/')
def index():
    return render_template('mail.html')


def async_send_mail(message):
    """异步发送邮件方法"""

    # 把应用上下文的环境开启
    with app.app_context():
        mail.send(message)


@app.route('/send_mail')
def send_mail():
    """发送邮件"""

    # 封装邮件内容
    message = Message()
    message.subject = '好久不见'
    message.recipients = ['897038924@qq.com']
    message.body = '你还好吗？'
    # html = None,

    # 发送邮件：阻塞式的，会阻塞响应
    # mail.send(message)

    # 使用子线程发送邮件
    thread = Thread(target=async_send_mail, args=(message,))
    thread.start()

    return '发送中。。'


if __name__ == '__main__':
    app.run(debug=True)