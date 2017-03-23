import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.base import Base, PHMixin


class OrganizationMDSLink(PHMixin, Base):
    __tablename__ = 'ph_organization_mds_links'

    organization_id = db.Column(db.Integer, db.ForeignKey("ph_organizations.id"))
    name = db.Column(db.String(50))
    url = db.Column(db.String(100))
    auth_token = db.Column(db.String(100))

    organization = relationship("Organization", back_populates="mds_links")
    protocols = relationship(
            "Protocol",
            secondary="ph_organization_mds_link_protocols",
            backref="mds_links",
    )
