import re

def validate_password(password):
    errors = []

    if len(password) < 8 or len(password) > 128:
        errors.append("Пароль должен быть от 8 до 128 символов.")
    if not re.search(r'[A-ZА-Я]', password):
        errors.append("Пароль должен содержать хотя бы одну заглавную букву.")
    if not re.search(r'[a-zа-я]', password):
        errors.append("Пароль должен содержать хотя бы одну строчную букву.")
    if not re.search(r'\d', password):
        errors.append("Пароль должен содержать хотя бы одну цифру.")
    if re.search(r'\s', password):
        errors.append("Пароль не должен содержать пробелов.")
    if not re.fullmatch(r'[A-Za-zА-Яа-я\d~!?@#$%^&*_\-+(){}\[\]<>/\\|"\'.:;,]+', password):
        errors.append("Пароль содержит недопустимые символы.")

    return errors
