# -*- coding:utf-8 -*-
from os import path, environ
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from werkzeug.routing import BaseConverter
from config import conifg


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
pagedown = PageDown()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'           # login_view设置登陆页面的端点
basedir = path.abspath(path.dirname(__file__))

def create_app(config_name):
    print '-------config_name:%s' % config_name
    app = Flask(__name__)
    app.config.from_object(conifg[config_name])   # 配置都在config.py这个文件中
    conifg[config_name].init_app(app)
    # app.url_map.converters['regex'] = RegexConverter
    # app.config.from_pyfile('config')
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'sqlite:///' + path.join(basedir, 'db.sqlite')
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # app.config['MAIL_SERVER'] = 'smtp.163.com'            # 配置163邮箱的smtp服务,首先你的邮箱要开启smtp服务
    # app.config['MAIL_PORT'] = 465                         # 端口为465
    # app.config['MAIL_USE_SSL'] = True                     # TLS服务失败，要用SSL
    # app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
    # app.config['FLASK_ADMIN'] = environ.get('FLASK_ADMIN')
    # app.config['POSTS_PER_PAGE'] = environ.get('POSTS_PER_PAGE')

    bootstrap.init_app(app)
    db.init_app(app)
    nav.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_1_0_blueprint    # 注册api蓝图
    app.register_blueprint(main_blueprint, static_folder='static', template_folder='templates')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1_0')

    @app.template_test('current_link')
    def current_link(link):
        return link == request.path

    return app

