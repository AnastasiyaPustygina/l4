import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

from app.config import TestingConfig, Config
from app.models.visit_logs import VisitLog
from app.models.user import User
from app.models.role import Role
from app.extensions import db

migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(testing=False):
    app = Flask(__name__)
    flask_env = os.getenv("FLASK_ENV", "production")

    if testing or flask_env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp, base_bp
    from app.routes.report_rotes import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(base_bp)
    app.register_blueprint(report_bp)

    login_manager.login_view = 'auth.login'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def log_visit():
        if request.endpoint != 'static':
            visit = VisitLog(path=request.path)
            if current_user.is_authenticated:
                visit.user_id = current_user.id
            db.session.add(visit)
            db.session.commit()

    # with app.app_context():
    #     users = User.query.all()
    #     print("Пользователи в базе:")
    #     for user in users:
    #         print(f"ID: {user.id}, Username: {user.username}, pass: {user.password_hash}")
    # with app.app_context():
    #     print("Роли в базе:")
    #     for role in Role.query.all():
    #         print(f"ID: {role.id}, Name: {role.name}, pass: {role.description}")

    return app