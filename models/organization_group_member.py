import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationGroupMember(PHMixin, Base):
    __tablename__ = 'ph_organization_group_members'

    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    organization_group_id = db.Column(db.Integer, db.ForeignKey('ph_organization_groups.id'))
