import sqlalchemy as db
from models.base import Base, PHBareMixin


class OrganizationGroupMember(PHBareMixin, Base):
    __tablename__ = 'ph_organization_group_members'

    organization_group_id = db.Column(
            db.Integer,
            db.ForeignKey('ph_organization_groups.id', ondelete='CASCADE'),
            primary_key=True)
    organization_member_id = db.Column(
            db.Integer,
            db.ForeignKey('ph_organization_members.id', ondelete='CASCADE'),
            primary_key=True)
