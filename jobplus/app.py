from flask import Flask
from jobplus.config import configs
from jobplus.models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager


def register_blueprints(app):
    """注册蓝图"""
    from .handlers import front
    app.register_blueprint(front)


def register_extensions(app):
    """将FLASK拓展注册到app"""
    # 初始化数据库
    db.init_app(app)
    Migrate(app, db)

    # 初始化LoginManager对象
    login_manager = LoginManager()
    login_manager.init_app(app)

    # 定义如何加载用户对象
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    # 当用login_required 装饰器保护一个路由时，如果用户未登录，就会被重定向到 login_view 指定的页面。
    login_manager.login_view = 'front.login'


def create_app(config):
    """app工厂"""
    # 创建app实例
    app = Flask(__name__)
    # 从python对象更新config配置
    app.config.from_object(configs.get(config))
    # 注册FLASK拓展到app
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    return app



