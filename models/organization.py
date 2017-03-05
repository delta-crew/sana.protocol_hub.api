import sqlalchemy as db
from models.base import Base, PHMixin


class Organization(PHMixin, Base):
    __tablename__ = 'ph_organization'

    # TODO
