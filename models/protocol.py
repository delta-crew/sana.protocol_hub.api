import sqlalchemy as db
from models.base import Base, PHMixin


class Protocol(PHMixin, Base):
    __tablename__ = 'ph_protocol'

    content = db.Column(db.String)
