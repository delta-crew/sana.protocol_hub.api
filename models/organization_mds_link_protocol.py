import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationMDSLinkProtocol(PHMixin, Base):
    __tablename__ = 'ph_organization_mds_link_protocol'

    # TODO
