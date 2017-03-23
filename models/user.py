import sqlalchemy as db
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    owned_organizations = relationship("Organization", back_populates="owner")
    organizations = relationship("Organization",
            secondary="ph_organization_members", backref="members")
