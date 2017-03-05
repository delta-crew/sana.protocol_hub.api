import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class Organization(PHMixin, Base):
    __tablename__ = 'ph_organizations'

    name = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))

    owner = relationship("User", back_populates="owned_organizations")
    groups = relationship("OrganizationGroup", back_populates="organization")
    mds_links = relationship("OrganizationMDSLink", back_populates="organization")
    members = relationship("User", secondary="OrganizationMember", backref="organizations")
    protocols = relationship("Protocol", secondary="SharedProtocol", backref="organizations")
