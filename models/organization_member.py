import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationMember(PHMixin, Base):
    __tablename__ = 'ph_organization_member'

    # TODO
