from functools import partial

from .config import load_config
from .operations import (
    create_new_db,
    create_table,
    create_column,
    create_mock
)

class Operations(object):
    def __init__(self, db_path):
        self.create_new_db = partial(create_new_db, db_path)
        self.create_table = partial(create_table, db_path)
        self.create_column = partial(create_column, db_path)
        self.create_mock = partial(create_mock, db_path)

class Pseudodb(object):
    def __init__(self):
        self.load_config()
        self.operations = Operations(self.config['db_path'])

    def load_config(self):
        self.config = load_config()

    def create_new_db(self, after_creation=None):
        self.operations.create_new_db()
        if after_creation is not None:
            after_creation()
    
    def create_table(self, name, after_creation=None):
        self.operations.create_table(name)
        if after_creation is not None:
            after_creation()
    
    def create_column(self, name, type, after_creation=None):
        pass

    def create_mock(self, name, headers, types, rows, after_creation=None):

        def after_creation(name, headers, types, rows):
            finished = """
                        Created new Mock table named %s
                        Table has %s rows of type %s
                        The column names are %s
                    """ % (name, rows, types, headers)
            print(finished)

        after_creation = after_creation(name, headers, types, rows)
        self.operations.create_mock(name, headers, types, rows, after_creation=after_creation)
        


    
    