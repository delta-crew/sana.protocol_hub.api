import sqlalchemy as db
from models.base import Base, PHMixin


class Protocol(PHMixin, Base):
    __tablename__ = 'ph_protocols'

    version = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
