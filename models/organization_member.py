import sqlalchemy as db
from models.base import Base, PHMixin


class OrganizationMember(PHMixin, Base):
    __tablename__ = 'ph_organization_member'

    organization_id = db.Column(db.Integer, db.ForeignKey("ph_organizations.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("auth_user.id"))
