from app.extensions import db

class Role(db.Model):

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128))
    users = db.relationship('User', backref='role', lazy=True)
