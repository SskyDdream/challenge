from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Base(db.Model):
    """基类，抽取相同的字段出来"""
    # 表示不要把这类当作是Model类
    __abstract__ = True
    created_time = db.Column(db.DateTime, default=datetime.utcnow())
    updated_time = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class User(Base, UserMixin):
    __tablename__ = 'user'

    # 用数值表示角色，方便判断是否有权限
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, ori_password):
        """ Python 风格的 setter, 这样设置 user.password 就会
            自动为 password 生成哈希值存入 _password 字段
        """
        self._password = generate_password_hash(ori_password)

    def check_password(self, password):
        """检测用户输入的密码和哈希密码是否一致"""
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

