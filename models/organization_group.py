import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationGroup(PHMixin, Base):
    __tablename__ = 'ph_organization_groups'

    organization_id = db.Column(
            db.Integer,
            db.ForeignKey('ph_organizations.id', ondelete='CASCADE'))
    name = db.Column(db.String(50))
    manage_mds = db.Column(db.Boolean)
    manage_mds_protocols = db.Column(db.Boolean)
    sync_with_mds = db.Column(db.Boolean)
    manage_groups = db.Column(db.Boolean)
    # rest of permissions...

    organization = relationship("Organization", back_populates="groups")
    members = relationship("OrganizationMember", secondary="OrganizationGroupMember", backref="groups")
