from flask import Blueprint, render_template, flash, url_for, redirect
from jobplus.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user
from jobplus.models import User, db

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
        company_user = form.create_user()
        company_user.role = User.ROLE_COMPANY
        db.session.add(company_user)
        db.session.commit()
        flash('注册成功', 'success')
        return redirect(url_for('front.login'))
    return render_template('companyregister.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash('该用户已被禁用', 'warning')
        else:
            login_user(user, form.remember_me.data)
            goto = 'user.profile'
            if user.is_admin:
                goto = '.index'
            elif user.is_company:
                goto = 'company.profile'
            return redirect(url_for(goto))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index'))