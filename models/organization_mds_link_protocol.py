import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationMDSLinkProtocol(PHMixin, Base):
    __tablename__ = 'ph_organization_mds_link_protocols'

    mds_link_id = db.Column(
            db.Integer,
            db.ForeignKey("ph_organization_mds_links.id", ondelete='CASCADE'),
            nullable=False)
    protocol_id = db.Column(
            db.Integer,
            db.ForeignKey("ph_protocols.id", ondelete='CASCADE'),
            nullable=False)
    synchronized_version = db.Column(
            db.Integer,
            db.ForeignKey("ph_protocols.version", ondelete='CASCADE'))
