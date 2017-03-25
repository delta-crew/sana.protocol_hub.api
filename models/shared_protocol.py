import sqlalchemy as db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from models.base import Base, PHMixin


class SharedProtocol(PHMixin, Base):
    __tablename__ = 'ph_shared_protocols'
    __table_args__ = (
        UniqueConstraint("protocol_id", "organization_id", name="po_1"),
    )

    protocol_id = db.Column(db.Integer)
    protocol_version = db.Column(db.Integer)
    organization_id = db.Column(db.Integer, db.ForeignKey("ph_organizations.id"))

    db.ForeignKeyConstraint(
            [protocol_id, protocol_version],
            ["ph_protocols.id", "ph_protocols.version"],
            ondelete="CASCADE")

    protocol = relationship(
            "Protocol",
            backref="shared_versions",
            foreign_keys=[protocol_version, protocol_id],
    )
    organization = relationship(
            "Organization",
            foreign_keys=[organization_id],
    )
