import configparser

from fastapi import Depends

def get_database_url():
    config = configparser.ConfigParser()
    config.readfp(open(r"./config/configfile.ini"))
    # SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
    user, password, host, port, db = get_config_variables(config)
    SQLALCHEMY_DATABASE_URL = "mysql://%s:%s@%s:%s/%s"%(user,password,host,port,db)
    return SQLALCHEMY_DATABASE_URL

def get_config_variables(config):
    user = config.get('mysql','user')
    password = config.get('mysql','password')
    host = config.get('mysql','host')
    port = config.get('mysql','port')
    db = config.get('mysql','db')
    return user,password,host,port,db

def get_config():
    config = configparser.ConfigParser()
    config.readfp(open(r"./config/configfile.ini"))
    return config

def get_config_param(param: str, config : configparser.ConfigParser = Depends(get_config)):
    return config.get('mysql',param)

