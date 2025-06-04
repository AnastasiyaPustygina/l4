from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import LoginForm, ChangePasswordForm
from app.models.user import User
from app import db
from werkzeug.security import *
from app.utils.validators import validate_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('user.index'))
        else:
            error_message = 'Неверный логин или пароль'
            flash(error_message, 'danger')
    return render_template('login.html', form=form, error_message=error_message)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Неверный старый пароль', 'danger')
        elif form.new_password.data != form.confirm_password.data:
            flash('Новые пароли не совпадают', 'danger')
        else:
            errors = validate_password(form.new_password.data)
            if errors:
                for error in errors:
                    flash(error, 'danger')
            else:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash('Пароль успешно изменён', 'success')
                return redirect(url_for('user.index'))
    return render_template('change_password.html', form=form)