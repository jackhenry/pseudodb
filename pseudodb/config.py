import os
import yaml
from schema import Use, Schema, SchemaError, Optional

class InvalidConfig(Exception):
    pass

default_config = {
    'db_path': '/mock.db',
    'row_count': 100
}
schema = Schema({
    'db_path': Use(str),
    'row_count': Use(int)
})

def get_config_path():
    config_folder = os.path.expanduser('~')
    config_path = os.path.join(config_folder, 'pseudodb.yaml')
    return config_path

def load_config():
    config = {}
    config_path = get_config_path()
    try:
        with open(
            get_config_path(),
            'rb'
        ) as c_file:
            config = yaml.safe_load(c_file)
        
        if not config:
            print("No config found")
            config = default_config
    except FileNotFoundError:
        config = default_config

    print(config)
    
    return schema.validate(config)

def save_config(config):
    with open(get_config_path(), 'w') as c_file:
        yaml.dump(config, c_file)

def set_config(key, value):
    config = load_config()
    config[key] = value
    try:
        schema.validate(config)
        save_config(config)
    except SchemaError as se:
        raise InvalidConfig(se)

    