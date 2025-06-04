
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, Optional
import re

class UserForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message="Поле не может быть пустым"),
        Length(min=5, message="Логин должен быть не менее 5 символов"),
        Regexp(r'^[A-Za-z0-9]+$', message="Логин должен содержать только латинские буквы и цифры")
    ])

    first_name = StringField('Имя', validators=[
        DataRequired(message="Поле не может быть пустым")
    ])

    last_name = StringField('Фамилия', validators=[
        DataRequired(message="Поле не может быть пустым")
    ])

    middle_name = StringField('Отчество')

    password = PasswordField('Пароль', validators=[Optional(),
        Length(min=8, max=128, message="Пароль должен быть от 8 до 128 символов")
    ])

    role_id = SelectField('Роль', coerce=int)
    submit = SubmitField('Сохранить')

    def validate_password(self, field):
        password = field.data
        if not password:
            return
        if " " in password:
            raise ValidationError("Пароль не должен содержать пробелов")
        if not re.search(r'^[A-Za-z0-9]+$', password):
            raise ValidationError("Пароль должен содержать только латинские буквы и цифры")
        if not re.search(r'[a-zа-я]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r'[A-ZА-Я]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'\d', password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
        if re.search(r'[^\w~!?@#$%^&*_\-+()\[\]{}<>/\\|\"\'.,:;]', password):
            raise ValidationError("Пароль содержит недопустимые символы")
