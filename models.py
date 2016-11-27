import sqlalchemy as db
import sqlalchemy.ext.declarative as db_ext
import sqlalchemy.orm as db_orm


Base = db_ext.declarative_base()


class PHMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now())

class Protocol(PHMixin, Base):
    __tablename__ = 'protocol'

    def __init__(self, **kwargs):
        kwargs.pop('content', None)
        super(Protocol, self).__init__(**kwargs)

    def get_content(self):
        return 'test'
