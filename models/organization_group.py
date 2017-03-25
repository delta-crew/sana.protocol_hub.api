import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationGroup(PHMixin, Base):
    __tablename__ = 'ph_organization_groups'

    organization_id = db.Column(
            db.Integer,
            db.ForeignKey('ph_organizations.id', ondelete='CASCADE'))
    name = db.Column(db.String(50))
    manage_protocols = db.Column(db.Boolean, default=False)
    manage_mds = db.Column(db.Boolean, default=False)
    manage_mds_protocols = db.Column(db.Boolean, default=False)
    synchronize_mds = db.Column(db.Boolean, default=False)
    manage_groups = db.Column(db.Boolean, default=False)
    manage_members = db.Column(db.Boolean, default=False)
    manage_ownership = db.Column(db.Boolean, default=False)
    # rest of permissions...

    organization = relationship("Organization")
    members = relationship(
            "OrganizationMember",
            secondary="ph_organization_group_members",
            back_populates="groups"
    )
