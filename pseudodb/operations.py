import sqlite3
import records
import os
import sys

from .mock import Mock
from .exceptions import TableExists
"""
All queries passed here where they are executed.
"""
def run_query(db_path, query):
    PREFIX = "sqlite:///"
    connection_url = PREFIX + db_path

    db = records.Database(connection_url)
    db.query(query)
"""
Create new db file
"""
def create_new_db(db_path):
    try:
        connection = sqlite3.connect(db_path)
        connection.close()
    except:
        print("Could not create database with path %s" % db_path)
        print("Double check the path and try again")
        sys.exit(1)

"""
Create table with name of passed argument. Create a ID field as a primary key. 
Ensure the table does not exist by calling internal table_exists method.
"""
def create_table(db_path, name):

    def table_exists(db_path, name):
        query = '''
                    SELECT * FROM %s;
                '''
        try:
            run_query(db_path, query % name)
            table_exists = True
        except:
            table_exists = False

        return table_exists

    query = '''
                CREATE TABLE IF NOT EXISTS %s (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT
                );
                    
            '''

    if table_exists(db_path, name):
        raise TableExists("Table %s already exists. Please delete if you would like to create a new table with that name." % name)
        sys.exit(1)
    else:
        run_query(db_path, query % name)

"""
Create single column in table with name and type
"""
def create_column(db_path, tbl_name, col_name, col_type):
    query = '''
                ALTER TABLE %s
                ADD %s %s
            '''

    run_query(db_path, query % (tbl_name, col_name, col_type))

"""
Function for inserting a row of values at a time in the table.
"""
def insert(db_path, tbl_name, columns, values):
    #Inner function prepares list of columns and values into SQL syntax
    #Adds commas to ever element except the trailing one.
    def prep_list_for_query(query_list):
        with_commas = ""
        for element in query_list:
            with_commas += "|" + "'" + element + "'"
        #Character at index 0 will be |. 
        #Retrieve substring starting at index 1 and replace occurences of |
        with_commas = with_commas[1:].replace("|", ",")
        return with_commas
    
    columns_query = prep_list_for_query(columns)
    values_query = prep_list_for_query(values)
    query = '''
                INSERT INTO %s (%s)
                VALUES
                    (%s)
            '''
    run_query(db_path, query % (tbl_name, columns_query, values_query))

"""
Create the mock table using passed arguments of header names, mock types and number of rows
"""
def create_mock(db_path, name, headers, types, rows, after_creation=None):
    mock = Mock()
    #Create table with provided name
    create_table(db_path, name)

    #Key is column name
    #Value is a list of mock data for the column name
    columns = {}
    table_specs = list(zip(headers, types))
    for spec in table_specs:
        column_name = spec[0]
        mock_type = spec[1]
        #create a column in the table for each name provided.
        create_column(db_path, name, column_name, mock.get_col_type(mock_type))
        #Get mock data for each row of the column. Put it in a list and map it to the column name in the dict
        columns[column_name] = list(map(lambda x: mock.get_mock_data(mock_type), range(0,rows)))

    for i in range(0, rows):
        #current row will be the ith element of each list in the columns dict
        current_row = [item[i] for item in columns.values()]
        #insert the row
        insert(db_path, name, headers, current_row)

    if after_creation is not None:
        after_creation()