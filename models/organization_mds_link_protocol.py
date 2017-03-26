import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationMDSLinkProtocol(PHMixin, Base):
    __tablename__ = "ph_organization_mds_link_protocols"

    mds_link_id = db.Column(
            db.Integer,
            db.ForeignKey("ph_organization_mds_links.id", ondelete="CASCADE"),
            nullable=False)
    protocol_id = db.Column(
            db.Integer,
            nullable=False)
    protocol_version = db.Column(
            db.Integer)
    synchronized_version = db.Column(
            db.Integer)

    db.ForeignKeyConstraint(
            [protocol_id, protocol_version],
            ["ph_protocols.id", "ph_protocols.version"],
            ondelete="CASCADE")

    protocol = relationship("Protocol")
