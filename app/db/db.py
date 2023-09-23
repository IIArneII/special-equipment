from config import DBConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def init_db(config: DBConfig):
    engine = create_engine(config.dsn())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
