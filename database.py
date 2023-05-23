from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

from config.config_getter import get_database_url

SQLALCHEMY_DATABASE_URL = get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    #, connect_args={"check_same_thread": False}        -- Not needed for other DB than SQLite
)
"""
engine_test = create_engine(
    SQLALCHEMY_DATABASE_TEST_URL
    #, connect_args={"check_same_thread": False}        -- Not needed for other DB than SQLite
)
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base = declarative_base()