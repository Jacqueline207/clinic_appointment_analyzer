#File to handle the connection to the database. SQLite DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase

#sets up SQL Alchemy to talk to local SQ Lite database called test.db
DATABASE_URL = "sqlite:///test.db"
#engine is the connection, metadata.create_all() creates tables later once models exist
#and sessionlocal is how the rest of the project will open sessions for database access
engine = create_engine(DATABASE_URL)
DBModelBase.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

