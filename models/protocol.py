import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHBareMixin


class Protocol(PHBareMixin, Base):
    __tablename__ = "ph_protocols"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
