from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, URL
from jobplus.models import db, User, CompanyDetail
from wtforms import ValidationError


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    # 自定义的表单数据验证器
    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱未注册")

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("密码错误")


class UserProfileForm(FlaskForm):
    real_name = StringField('姓名')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码(不填保持不变)')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume_url = StringField('简历的链接')
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        number_start = ('13', '14', '15', '16', '17', '18', '19')
        if len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

        if phone[:2] not in number_start:
            raise ValidationError('请输入有效的手机号')

    def update_user(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    '''企业名称、邮箱、手机号、密码，地址，logo图片链接，网站链接，一句话简介，详细介绍'''
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码(不填保持不变)')
    phone = StringField('手机号')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 24)])
    logo = StringField('Logo', validators=[Length(0, 64)])
    site = StringField('网站链接',  validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 100)])
    about = StringField('详细介绍', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def update_user(self, user):
        user.username = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_detail:
            company_detail = user.company_detail
        # 企业第一次填充资料时，创建CompanyDetail对象，找出与用户对应的数据，使用表单数据填充
        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id

        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()


class EditUserForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码')
    real_name = StringField('姓名')
    phone = StringField('手机号')
    submit = SubmitField('提交')

    def update(self, user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()


class EditCompanyForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码')
    phone = StringField('手机号')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 100)])
    logo = StringField('logo', validators=[DataRequired()])
    submit = SubmitField('提交')

    def update(self, company):
        company.username = self.name.data
        company.email = self.email.data
        company.phone = self.phone.data
        if self.password.data:
            company.password = self.password.data

        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id

        detail.site = self.site.data
        detail.description = self.description.data
        detail.logo = self.logo.data

        db.session.add(company)
        db.session.add(detail)
        db.session.commit()







