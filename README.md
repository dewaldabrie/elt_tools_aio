# ELT-Tools-AIO
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b)](https://github.com/dewaldabrie/elt_tools_aio/issues)
[![GitHub Stars](https://img.shields.io/github/stars/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorB=ebcb8b&colorA=4c566a)](https://github.com/dewaldabrie/elt_tools_aio/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b)](https://github.com/dewaldabrie/elt_tools_aio/network)

## Database Abstraction

A set of tools to serve as an abstraction layer over many commonly used databases, as long
as it's supported by SQLAlchemy. It supports the following operations in an easy-to-use 
interface:

* asynchronous (non-blocking) operation
* count the number of rows in a table
* find duplicates in a table
* find records missing in target with respect to source
* find records on target which have been hard deleted from source
* execute a sql query against a table

## ELT Pair Operations

In Extract-Load-Transform (ELT) operations, a table is extracted and loaded from one database
to another with potential transformations after that (for example in a database view). This is
akin to database replication, albeit not necessarily all tables nor all columns are transferred. 
One may also only transfer records from a certain date onwards. 

[comment]: <> ( ![alt text]\(images/source-target-venn.svg?raw=true\) )
<img src="images/source-target-venn.svg" alt="source-target-records-venn" width="400" height="400">

Many common database engineering tasks relate to the source and target pairs. This library 
assists by implementing these commonly performed operations in a succinct interface such as:

* show a list of common tables between source and target database
* compare counts between source and target tables over a specified time window
* find primary keys of missing records in the target
* fill missing records into the target over a given date range
* find primary keys of orphaned records in the target (i.e. corresponding records from the 
  source database have been deleted)
* remove orphaned records from target (even for large tables)

## Configuration and Examples
The library provides two main classes: `DataClient` for database abstraction and `ELTDBPair` for 
ELT operations between database pairs. The user passes configuration dictionaries into these classes.
The configuration describes database credentials, and details of which databases to pair up. 

For example, to find duplicate on a particular table:

```python
import asyncio
from os import environ
from elt_tools_aio.client import DataClientFactory

DATABASES = {
    'db_key11': {
        'engine': 'oltp_engine',
        'sql_alchemy_conn_string': environ.get('mysql_db_uri'),
    },
    'db_key12': {
        'engine': 'bigquery_engine',
        'dataset_id': 'mydata',
        'gcp_project': environ.get('GCP_PROJECT'),
        'gcp_credentials': environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
    },
}

async def print_duplicate_keys():
    factory = DataClientFactory(DATABASES)
    client = factory(db_key='db_key11')
    customer_duplicates = await client.find_duplicate_keys('customers', 'id')
    print(customer_duplicates)


asyncio.run(print_duplicate_keys())
```

For example, to remove orphaned records on the target table of a particular ELT Pair
using a binary search strategy on a large table:

```python
import asyncio
from os import environ
from elt_tools_aio.client import ELTDBPairFactory

DATABASES = {
    'db_key11': {
        'engine': 'oltp_engine',
        'sql_alchemy_conn_string': environ.get('mysql_db_uri'),
    },
    'db_key12': {
        'engine': 'bigquery_engine',
        'dataset_id': 'mydata',
        'gcp_project': environ.get('GCP_PROJECT'),
        'gcp_credentials': environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
    },
}
ELT_PAIRS = {
    'pair1': {
        'source': 'db_key11', 'target': 'db_key12'
    },
}

async def remove_orphans():
    factory = ELTDBPairFactory(ELT_PAIRS, DATABASES)
    elt_pair = factory(pair_key='pair1')
    _ = await elt_pair.remove_orphans_from_target_with_binary_search(
        'customers', 
        'id', 
        timestamp_fields=['created_at']
    )

asyncio.run(remove_orphans())
```

## Installation instructions

```shell
$ pip install git+ssh://git@github.com/dewaldabrie/elt_tools_aio.git
```

