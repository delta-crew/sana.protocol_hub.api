import sqlalchemy as db
import sqlalchemy.ext.declarative as db_ext


Base = db_ext.declarative_base()


class PHBareMixin(object):
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now())


class PHMixin(PHBareMixin, object):
    id = db.Column(db.Integer, primary_key=True)
