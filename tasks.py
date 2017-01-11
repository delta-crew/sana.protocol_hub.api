import os

from app.db import engine
from models import Base

from invoke import task


@task
def create_db(ctx):
    Base.metadata.create_all(engine)

@task
def drop_db(ctx):
    Base.metadata.drop_all(engine)

@task
def reset_db(ctx):
    drop_db(ctx)
    create_db(ctx)
