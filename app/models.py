from app import db

class URL(db.Model):
    __tablename__ = 'URL'
    id = db.Column(db.Integer, primary_key=True)
    full = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(255), nullable=False, unique=True)
    clicks = db.Column(db.Integer, default=0)
    user = db.Column(db.String(255), nullable=False)