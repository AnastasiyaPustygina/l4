from flask import Blueprint, render_template, send_file, request
from flask_login import current_user
from sqlalchemy import func
from app.models.visit_logs import VisitLog
from app.models.user import User
from app.utils.checker_rights import check_rights
import csv
import io

def get_db():
    from app import db
    return db

db = get_db()

report_bp = Blueprint('report', __name__, url_prefix='/report')


@report_bp.route('/logs')
@check_rights(['admin', 'user'])
def logs():
    page = request.args.get('page', 1, type=int)
    query = VisitLog.query.order_by(VisitLog.created_at.desc())

    if current_user.role.name == 'user':
        query = query.filter_by(user_id=current_user.id)

    logs = query.paginate(page=page, per_page=10)
    return render_template('logs.html', logs=logs)

@report_bp.route('/by-pages')
@check_rights(['admin'])
def by_pages():
    stats = db.session.query(
        VisitLog.path,
        func.count().label('count')
    ).group_by(VisitLog.path) \
     .order_by(func.count().desc()).all()
    return render_template('report_by_pages.html', stats=stats)

@report_bp.route('/by-pages/export')
@check_rights(['admin'])
def export_by_pages():
    stats = db.session.query(
        VisitLog.path,
        func.count().label('count')
    ).group_by(VisitLog.path) \
     .order_by(func.count().desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Страница', 'Количество посещений'])

    for path, count in stats:
        writer.writerow([path, count])

    output.seek(0)
    return send_file(
        io.BytesIO(output.read().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='pages_report.csv'
    )


@report_bp.route('/by-users')
@check_rights(['admin'])
def by_users():
    stats = db.session.query(
        User.username,
        func.count(VisitLog.id).label('count')
    ).outerjoin(VisitLog) \
     .group_by(User.id) \
     .order_by(func.count(VisitLog.id).desc()).all()

    return render_template('report_by_users.html', stats=stats)