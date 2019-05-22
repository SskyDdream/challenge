from flask import Blueprint, render_template, flash, url_for, redirect
from jobplus.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user
from jobplus.models import User

front = Blueprint('front', __name__)


@front.route('/')
def index():
    return render_template('index.html')


@front.route('/userregister', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    # 判断表单数据是否正确和是否提交
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功', 'success')
        return redirect(url_for('front.login'))
    return render_template('userregister.html', form=form)


@front.route('/companyregister', methods=['GET', 'POST'])
def company_register():
    form = RegisterForm()
    form.username.label = u'企业名称'

    if form.validate_on_submit():
        form.create_user()
        flash('注册成功', 'success')
        return redirect(url_for('front.login'))
    return render_template('companyregister.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index'))