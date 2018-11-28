# ddb
 A sql interface for flat files written in python 


## Install
```
pip install ddb
# OR
pipenv install ddb
```

### Commandline interface
```
ddb
# OR
ddb --config-dir --query 'select * from `tablename` where column=value limit 0,10'
```

### Code integration
```
import ddb

e=ddb.engine('config_dir')

results=e.query('select * from `tablename` where column=value limit 0,10')


```


### Query support
- Query support is limited. As needed I'll improve the system.
- If you're doing vastly comlicated things, it shouldn't be with a flat file.
- This code is slow. It will be refactored, but not until more support is added.


### Supported Querys
- SELECT [COLUMNS] FROM [Table] [WHERE] [ORDER BY] [LIMIT]
- INSERT INTO [TABLE] ([COLUMNS]) VALUES ([VALUES])
- DELETE FROM [TABLE] [WHERE] 
- UPDATE [TABLE] SET [[COLUMN=VALUE]] [WHERE]
- SHOW COLUMNS
- SHOW TABLES

### Not supported
- Right now this is a POC, complex operations are not supported, but are in the works.
- JOIN, COUNT, SUM, DISTINCT, GROUP BY are all high on the list


### Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/data/ddb-demo.gif)

