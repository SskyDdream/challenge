class BaseConfig(object):
    """配置基类"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'very secret key'


class DevelopmentConfig(BaseConfig):
    """开发环境"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig
}