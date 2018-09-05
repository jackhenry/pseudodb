# pseudodb
Generate mock sqlite tables quickly.

## Why?
Sometimes you just need a table of data. Maybe you are testing an algorithm, learning a new library or need a stand-in. pseudodb is a simple command line tool that creates mock sqlite tables. You can specify the column names, the type of data in each column and the ammount of rows in the table.

## Installing
(pip package coming soon)
```
git clone https://github.com/jackhenry/pseudodb
cd pseudodb
pip install -r requirements.txt
python setup.py install
```

## Usage
Use the new argument to specify the .db file you would like to create the mock tables in. This will create a new .db file if the file does not already exist. **IMPORTANT** Make sure your path ends with the name of the db file.
```
pseudodb new ~/mock.db
```

Use the create argument to create a mock table. The table will be created in the .db file you specified with the new argument. 
```
pseudodb create my_mock_table FIRST_NAME,LAST_NAME,BIRTHDAY,SALARY firstname,lastname,date,dollars --rows=250
```
* **my_mock_table** - This argument is the name the table will be given
* **FIRST_NAME,LAST_NAME,BIRTHDAY,SALARY** - Indicates the table will have 4 columns with those names. Names are delimited by columns
* **firstname,lastname,date,dollars** - These are mock types. This will tell pseudodb what kind of values to randomly generate
* **--rows** - The amount of rows with random data the table will contain **(optional)**
