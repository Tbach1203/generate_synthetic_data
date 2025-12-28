from configparser import ConfigParser
import psycopg2

def load_config(filename='config/database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section) 
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config

def connect(config):
    try:
        conn = psycopg2.connect(**config)
        print("Connect successfull!")
    except (psycopg2.DatabaseError, Exception) as e:
        print(e)
    return conn