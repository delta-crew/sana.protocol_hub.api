import config

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(config.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
