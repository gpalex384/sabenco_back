import configparser
import MySQLdb
from sqlalchemy import text

from database import engine

def restore_test_database():
    ################
    # Restore database
    ################
    # Read sql files
    schema = open('./sql/restore_test_schema.sql')
    sql_schema = schema.read()
    schema.close()
    triggers = open('./sql/restore_triggers.sql')
    sql_triggers = triggers.read()
    triggers.close() 
    data = open('./sql/restore_test_data.sql')
    sql_data = data.read()
    data.close() 

    # Create lists of sql statements
    sql_schema_commandslist = sql_schema.split(';')
    sql_triggers_commandslist = sql_triggers.split('$')
    sql_data_commandslist = sql_data.split(';')

    # Loop and execute sql statements lists
    conn = engine.connect()
    for command in sql_schema_commandslist:
        try:
            conn.execute(text(command))
        except MySQLdb.OperationalError:
            print("Command skipped: " + command)
    for command in sql_triggers_commandslist:
        try:
            conn.execute(text(command))
        except MySQLdb.OperationalError:
            print("Command skipped: " + command)
    for command in sql_data_commandslist:
        try:
            conn.execute(text(command))
        except MySQLdb.OperationalError:
            print("Command skipped: " + command)
    conn.close()

