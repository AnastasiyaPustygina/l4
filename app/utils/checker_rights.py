from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def check_rights(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))

            if current_user.role.name not in allowed_roles:
                flash('У вас недостаточно прав для доступа к этой странице.', 'danger')
                return redirect(url_for('base.index'))

            return view_func(*args, **kwargs)
        return wrapper
    return decorator