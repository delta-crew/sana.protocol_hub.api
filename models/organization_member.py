import sqlalchemy as db
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationMember(PHMixin, Base):
    __tablename__ = 'ph_organization_members'
    __table_args__ = (
        UniqueConstraint('organization_id', 'user_id'),
    )

    organization_id = db.Column(
            db.Integer,
            db.ForeignKey("ph_organizations.id", ondelete='CASCADE'))
    user_id = db.Column(
            db.Integer,
            db.ForeignKey("auth_user.id"))

    user = relationship("User")
    organization = relationship("Organization")
    groups = relationship(
            "OrganizationGroup",
            secondary="ph_organization_group_members",
            back_populates="members",
    )
