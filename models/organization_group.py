import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationGroup(PHMixin, Base):
    __tablename__ = 'ph_organization_group'

    # TODO
