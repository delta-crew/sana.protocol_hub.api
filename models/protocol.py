import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHBareMixin


class Protocol(PHBareMixin, Base):
    __tablename__ = "ph_protocols"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    content = db.Column(db.String)
    public = db.Column(db.Boolean, default=False)
