from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import User, db
from flask_login import current_user
from jobplus.forms import RegisterForm, EditUserForm, EditCompanyForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users/')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/users/adduser', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('创建普通用户成功', 'success')
        return redirect(url_for('.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/addcompany', methods=['GET', 'POST'])
@admin_required
def create_company():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('创建企业用户成功', 'success')
        return redirect(url_for('.users'))
    return render_template('admin/create_company.html', form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        form = EditCompanyForm(obj=user)

    else:
        form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.update(user)
        flash('用户信息更新成功', 'success')
        return redirect(url_for('.users'))

    if user.is_company:
        form.name.data = user.username
        form.site.data = user.detail.site
        form.description.data = user.detail.description
        form.logo.data = user.detail.logo
    return render_template('admin/edit_user.html', user=user, form=form)


@admin.route('/users/<int:user_id>/disable', methods=['GET', 'POST'])
@admin_required
def disable(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('已经成功启用用户', 'success')
    else:
        user.is_disable = True
        flash('已经成功禁用用户', 'success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('.users'))












