import sqlalchemy as db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from models.base import Base, PHMixin


class SharedProtocol(PHMixin, Base):
    __tablename__ = 'ph_shared_protocols'
    __table_args__ = (
        UniqueConstraint("protocol_id", "organization_id", name="po_1"),
    )

    protocol_id = db.Column(db.Integer, db.ForeignKey("ph_protocols.id"))
    protocol_version = db.Column(db.Integer, db.ForeignKey("ph_protocols.version"))
    organization_id = db.Column(db.Integer, db.ForeignKey("ph_organizations.id"))

    protocol = relationship("Protocol", back_populates="shared_versions")
    organization = relationship("Organization", back_populates="shared_protocols")
