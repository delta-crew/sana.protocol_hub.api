import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHBareMixin


class Protocol(PHBareMixin, Base):
    __tablename__ = "ph_protocols"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    version = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("auth_user.id"))

    user = relationship("User", backref="protocols")

    def previous_version(self, session):
        if self.version == 1:
            return None
        return session.query(Protocol).filter_by(version=self.version-1).first()
