from configparser import ConfigParser

def set_database_uri(app, database_name):
    config_template = ConfigParser()
    config_template.read('config.ini')

    db_uri_template = config_template.get('database', 'db_uri')
    db_uri = db_uri_template.format(database_name=database_name)

    print(db_uri)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri