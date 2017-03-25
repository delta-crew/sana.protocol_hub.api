import os

from app.db import engine
from models import Base, User, Token

from invoke import task


BUILDER_TABLENAMES = [
    User.__tablename__,
    Token.__tablename__,
]

HUB_TABLES = filter(
    lambda t: t.name not in BUILDER_TABLENAMES,
    Base.metadata.sorted_tables)

def create_tables(tables):
    Base.metadata.create_all(bind=engine, tables=tables)

def drop_tables(tables):
    Base.metadata.drop_all(bind=engine, tables=tables)

def reset_tables(tables):
    create_tables(tables)
    drop_tables(tables)

@task
def create_db(ctx):
    create_tables(HUB_TABLES)

@task
def drop_db(ctx):
    drop_tables(HUB_TABLES)

@task
def reset_db(ctx):
    reset_tables(HUB_TABLES)

@task
def create_entire_db(ctx):
    create_tables(None)

@task
def drop_entire_db(ctx):
    drop_tables(None)

@task
def reset_entire_db(ctx):
    reset_tables(None)
