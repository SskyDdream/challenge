from flask import Blueprint, redirect, url_for, render_template, flash, request, current_app
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm
from jobplus.models import CompanyDetail

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if not current_user.is_company:
        flash('您不是企业用户', 'warning')
        return redirect(url_for('front.index'))
        # 为什么是current_user.company_detail
    # form = CompanyProfileForm(obj=current_user.company_detail)
    form = CompanyProfileForm(obj=current_user.company_detail)
    form.name.data = current_user.username
    form.email.data = current_user.email
    # form.slug.data = current_user.company_detail.slug
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)


@company.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = CompanyDetail.query.order_by(CompanyDetail.created_time.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='company')