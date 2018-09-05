import logging
import os
import yaml
from schema import Use, Schema, SchemaError, Optional

logger = logging.getLogger(__name__)

class InvalidConfig(Exception):
    pass

default_config = {
    'db_path': '/mock.db',
    'row_count': 100,
    'logging': 0
}
schema = Schema({
    'db_path': Use(str),
    'row_count': Use(int),
    'logging': Use(int)
})

def get_config_path():
    cwd = os.getcwd()
    config_path = os.path.join(cwd, 'pseudodb.yaml')
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

    logger.debug('config loaded: %s' % config)

    return schema.validate(config)

def save_config(config):
    with open(get_config_path(), 'w') as c_file:
        yaml.dump(config, c_file)
        logger.debug('config saved to %s' % get_config_path())

def set_config(key, value):
    config = load_config()
    config[key] = value
    try:
        schema.validate(config)
        save_config(config)
    except SchemaError as se:
        raise InvalidConfig(se)

    