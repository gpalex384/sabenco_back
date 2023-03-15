import configparser

config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('mysql')
config.set('mysql', 'host', 'localhost')
config.set('mysql', 'user', 'ejemplo')
config.set('mysql', 'port', '3306')
config.set('mysql', 'password', 'ejemplo')
config.set('mysql', 'db', 'sabenco_back')

config.add_section('user_info')
config.set('user_info', 'admin', 'alex')
config.set('user_info', 'login', 'alex')
config.set('user_info', 'password', 'xela')

# Write the new structure to the new file
with open(r".\configfile.ini", 'w') as configfile:
    config.write(configfile)