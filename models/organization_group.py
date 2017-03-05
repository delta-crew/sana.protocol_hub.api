import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationGroup(PHMixin, Base):
    __tablename__ = 'ph_organization_groups'

    organization_id = db.Column(db.Integer, db.ForeignKey('ph_organizations.id'))
    name = db.Column(db.String(50))
    add_and_remove_members_permission = db.Column(db.Boolean)
    sync_with_mds_permission = db.Column(db.Boolean)
    # rest of permissions...

    organization = relationship("Organization", back_populates="groups")
    members = relationship("User", secondary="OrganizationGroupMember", backref="groups")
