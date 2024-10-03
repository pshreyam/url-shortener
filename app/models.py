import uuid

from app import db


class URL(db.Model):
    __tablename__ = "URL"

    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    full = db.Column(db.String(255), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    user = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<URL | full={self.full} | id={self.id}>"
