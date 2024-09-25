#!/usr/bin/env python
'''
Script to export full CMIP7 data request content from Airtable.

Usage examples:
    ./airtable_export.py -t my_token_file   # save output to a default filename that includes a timestamp
    ./airtable_export.py -t my_token_file -f dreq_raw_export.json   # save output to the indicated file
'''
import os
import json
import datetime
import argparse
from pyairtable import Api

filepath = '../content/airtable_export/dreq_raw_export_{timestamp}.json'

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filepath', type=str, default=filepath, help=\
                    f'Filepath at which to store exported Airtable content, default: {filepath}')
parser.add_argument('-t', '--token', type=str, help=\
                    'Path to text file containing Airtable token (required)')
args = parser.parse_args()

# Record date & time of this export
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%SsUTC')

# Get Airtable key string.
# This allows pyairtable to access Airtable and download content from all the bases that are accessible via this key.
if not os.path.exists(args.token):
    raise Exception(f'Airtable token file not found: {args.token}')
with open(args.token, 'r') as f:
   lines = [s.strip() for s in f.readlines()]
   lines = [s for s in lines if s not in [''] and not s.startswith('#')] # comment lines start with '#'
   assert len(lines) == 1, 'Expected only one non-comment non-empty line in file containing the Airtable key string'
   keyr = lines[0]
   print(f'Accessing Airtable using token {args.token}')

# Access Airtable using the key
api = Api(keyr)

bases = {} # Dict to store content of all bases accessed by the key
for base in api.bases():
    assert base.name not in bases, f'--> base {base.name} is already defined!'
    print(f'Adding base: {base.name}')

    tables = {} # Dict to store content of all tables in this base
    for table in base.tables():
        assert table.name not in tables, f'--> table {table.name} is already defined!'

        tables[table.name] = {
            'base_id' : base.id, # unique id string of the base, example: 'appBWxP0SS7K1hweJ'
            'base_name' : base.name, # human-readable name of the base
            'id' : table.id, # unique id string of the table, example: 'tbl7L210y9LFpFI7b'
            'name' : table.name, # human-readable name of the table
            'description' : '',
            'records' : {}, # dict to contain all records (rows) in the table, indexed by each record's unique id string
            'fields' : {}, # dict to contain schema info about the fields found in each record
        }

        schema = table.schema()
        if schema.description is not None:
            tables[table.name]['description'] = str(schema.description)

        # Get schema info about the fields contained in each of the records
        # Each field is identifed by a unique field i string, example: 'fld5T0XjDAdQ3fsVI'
        fields = tables[table.name]['fields']
        for field in schema.fields:
            assert field.id not in fields
            fields[field.id] = {
                'description' : field.description,
                'name' : field.name,
                'type' : field.type,
            }
            if hasattr(field, 'options') and hasattr(field.options, 'linked_table_id'):
                fields[field.id].update({
                    'linked_table_id' : field.options.linked_table_id
                })

        # Get all records in the table
        # Each record is identified by a unique record id string, example: 'rec00yWOulzoqJuY7'
        records = tables[table.name]['records']
        for record in table.all():
            assert record['id'] not in records
            records[ record['id'] ] = record['fields']

        nrec = len(records)
        print(f'  Added table {table.name} with {nrec} records')

    bases[base.name] = tables
    del tables

filepath = args.filepath.format(timestamp=timestamp)
with open(filepath, 'w') as f:
    json.dump(bases, f, sort_keys=True, indent=4)
    print(f'Wrote {filepath}')
