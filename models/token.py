import sqlalchemy as db

from models.base import Base


class Token(Base):
    __tablename__ = 'authtoken_token'

    key = db.Column(db.String, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('auth_user.id'),
        nullable=False)
