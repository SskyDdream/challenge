from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Base(db.Model):
    """基类，抽取相同的字段出来"""
    # 表示不要把这类当作是Model类
    __abstract__ = True
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# User和Job的中间表
user_job = db.Table('user_job',
                    db.Column('user_id', db.ForeignKey('user.id', ondelete='CASCADE')),
                    db.Column('job_id', db.ForeignKey('job.id', ondelete='CASCADE'))
                    )


class User(Base, UserMixin):
    __tablename__ = 'user'

    # 用数值表示角色，方便判断是否有权限
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    real_name = db.Column(db.String(32), unique=True, index=True, )
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    phone = db.Column(db.String(11), )
    work_years = db.Column(db.SmallInteger)
    # 用户上传的简历链接
    resume_url = db.Column(db.String(64))
    is_disable = db.Column(db.Boolean, default=False)
    # 企业用户详情
    detail = db.relationship('CompanyDetail', uselist=False)

    collect_jobs = db.relationship('Job', secondary=user_job)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

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
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class CompanyDetail(Base):
    __tablename__ = 'company_detail'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    logo = db.Column(db.String(128), nullable=False)
    site = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(124), nullable=False)
    # 一句话描述公司
    description = db.Column(db.String(100))
    # 公司的详情描述
    about = db.Column(db.String(1024))
    # 公司标签
    tags = db.Column(db.String(128))
    # 公司技术栈
    stack = db.Column(db.String(128))
    # 团队介绍
    team_introduction = db.Column(db.String(256))
    # 公司领域
    field = db.Column(db.String(128))
    # 融资进度
    finance_stage = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"))
    user = db.relationship('User', uselist=False, backref=db.backref('company_detail', uselist=False))

    def __repr__(self):
        return '<Company_detail:{}>'.format(self.id)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(24))
    # 职位标签， 多个标签用逗号分割
    tags = db.Column(db.String(128))
    experience_requirement = db.Column(db.String(32))
    degree_requirement = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)
    # 是否在招聘
    is_open = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
    views_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Job:{}>".format(self.name)

    @property
    def tag_list(self):
        return self.tags.split(',')






