import click

from .app import Pseudodb
from .operations import create_new_db, create_column
from .config import set_config
from .exceptions import InvalidInput

def get_app():
    app = Pseudodb()
    return app

@click.group()
def pseudodb():
    """Create mock Sqlite tables for testing """
    pass

@pseudodb.command(options_metavar='')
@click.argument('path', required=True, metavar='<path>')
def use(path):
    """
    Select .db file to use. Will create a new one if path doesn't exist
    
    Path is full path to new db file including file name
    
    Example: pseudodb new C:/User/John/DB/mysqlite.db
    """
    set_config('db_path', path)
    def after_creation(path):
        print("""
                Created new database: %s
             """ % (path))

    after_creation = after_creation(path)

    app = get_app()
    app.create_new_db(after_creation)

@pseudodb.command()
@click.argument('name', required=True)
@click.argument('headers', required=True)
@click.argument('types', required=True)
@click.option('--path')
@click.option('--rows')
def create(name, headers, types, path, rows):
    """
    Create a new mock table
    
    Example:
    """
    if path is not None:
        set_config('db_path', path)

    headers_list = headers.split(',')
    type_list = types.split(',')
    if len(headers_list) is not len(type_list):
        raise InvalidInput("headers and types are not the same length")
        sys.exit(1)


    app = get_app()
    if rows is None:
        rows = app.config['row_count']  
        
    app.create_mock(name, headers=headers_list, types=type_list, rows=int(rows))

def main():
    pseudodb()

if __name__ == '__main__':
    pseudodb()