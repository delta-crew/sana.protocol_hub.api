import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationMDSLink(PHMixin, Base):
    __tablename__ = 'ph_organization_mds_link'

    # TODO
