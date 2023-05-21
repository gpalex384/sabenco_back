from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.readfp(open(r"./config/configfile.ini"))
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
user = config.get('mysql','user')
password = config.get('mysql','password')
host = config.get('mysql','host')
port = config.get('mysql','port')
db = config.get('mysql','db')
SQLALCHEMY_DATABASE_URL = "mysql://%s:%s@%s:%s/%s"%(user,password,host,port,db)

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