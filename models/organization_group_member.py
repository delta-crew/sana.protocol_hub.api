import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationGroupMember(PHMixin, Base):
    __tablename__ = 'ph_organization_group_member'

    # TODO
