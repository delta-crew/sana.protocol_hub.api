import sqlalchemy as db
import sqlalchemy.ext.declarative as db_ext


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
