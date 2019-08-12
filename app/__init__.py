import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect # 导入csrf校验模块,csrfProtect在1.0之后移除
# from flask_cache import Cache

pymysql.install_as_MySQLdb()


# 惰性加载
csrf = CSRFProtect()

db = SQLAlchemy()

# cache = Cache()

def create_app(config_name):
    # 创建flask App实例
    app = Flask(__name__)
    # 使用类配置加载
    app.config.from_object('settings.DebugConfig')

    # app惰性加载插件
    csrf.init_app(app)
    db.init_app(app)
    # cache.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    from .ApiResource import api_main
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_main,url_prefix='/api')
    return app





