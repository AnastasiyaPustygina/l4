from types import NoneType

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from app.models.user import User
from app.models.role import Role
from app.forms.user_forms import UserForm
from app import db, VisitLog
from app.utils.checker_rights import check_rights

user_bp = Blueprint('user', __name__, url_prefix='/user')
base_bp = Blueprint('base', __name__)

class DeleteForm(FlaskForm):
    pass

@base_bp.route('/')
def index():
    users = User.query.all()
    form = DeleteForm()
    return render_template('index.html', users=users, form=form, current_user=current_user)


@user_bp.route('/')
@login_required
@check_rights(['admin'])
def index():
    users = User.query.all()
    form = DeleteForm()
    return render_template('index.html', users=users, form=form, current_user=current_user)


@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_rights(['admin'])
def create_user():
    form = UserForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            role_id=form.role_id.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('user успешно создан', 'success')
        print("Form validation errors:", form.errors)
        return redirect(url_for('user.index'))

    print("Form validation errors:", form.errors)
    return render_template('user_form.html', form=form)


@user_bp.route('/<int:user_id>')
@login_required
@check_rights(['admin', 'user'])
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role.name == 'user' and user.id != current_user.id:
        flash('Вы не можете редактировать других пользователей.', 'danger')
        return redirect(url_for('user.index'))
    return render_template('user_view.html', user=user)


@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights(['admin', 'user'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role.name == 'user' and user.id != current_user.id:
        flash('Вы не можете редактировать других пользователей.', 'danger')
        return redirect(url_for('user.index'))

    form = UserForm(obj=user)

    if current_user.role.name == 'user':
        del form.role_id
    else:
        form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    del form.password
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        if hasattr(form, 'role_id') and form.role_id is not None:
            user.role_id = form.role_id.data
        db.session.commit()
        flash('Данные пользователя обновлены', 'success')
        return redirect(url_for('user.index'))

    return render_template('user_form.html', form=form, user=user)


@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
@check_rights(['admin'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Нельзя удалить самого себя!', 'danger')
        return redirect(url_for('user.index'))
    VisitLog.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('user удалён', 'success')
    return redirect(url_for('user.index'))
