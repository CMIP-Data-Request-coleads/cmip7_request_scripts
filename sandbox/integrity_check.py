#!/usr/bin/env python
'''
Check integrity of record links in raw airtable export.

First need to run airtable_export.py to produce the raw airtable export. 
This saves the 'bases' dict to a json file.
'''
import json

try: bases
except:
    filepath = 'latest.json'
    with open(filepath, 'r') as f:
        bases = json.load(f)
        print(f'Opened {filepath}')

# Show names of bases, their tables, and number of records in each table
for base_name, tables in bases.items():
    print(base_name)
    for table_name, table in tables.items():
        nrec = len(table['records'])
        print(f'  {table_name}  ({nrec} records)')


def check_id(uid : str, uid_type : str) -> bool:
    '''
    Return True if input string uid has the expected format for unique identifiers in an airtable export via pyairtable.
    Example: 'rec00yWOulzoqJuY7' (for a record id string)
    '''
    uid_prefix = {'record' : 'rec', 'field' : 'fld', 'base' : 'app', 'table' : 'tbl'}
    prefix = uid_prefix[uid_type]
    return isinstance(uid, str) and uid.startswith(prefix) and len(uid) == 17

# Check integrity of record links in each base
for base_name, tables in bases.items():
    print('\n' + base_name)

    table_id2name = {table['id'] : table['name'] for table in tables.values()} # given table id, look up table name
    n = len(tables)
    assert len(set(table_id2name.keys())) == n, 'table ids are not unique'
    assert len(set(table_id2name.values())) == n, 'table names are not unique'

    # For the tables in this base, check that linked records point to valid records in the indicated linked table
    for table_name, table in tables.items():
        print(table_name)

        # Make dict with info on fields, indexed by field name (instead of field id)
        fields = {}
        for field_id, field in table['fields'].items():
            name = field['name']
            assert name not in fields, 'field names are not unique'
            fields[name] = field

        records = table['records']
        for record in records.values():
            for name in record:
                field = fields[name]
                if 'linked_table_id' in field:
                    # This field in the record contains a list of links to records in another table
                    record_links = record[name]  # list of record ids
                    assert isinstance(record_links, list), 'links to other records should be in a list'
                    assert all([check_id(uid, 'record') for uid in record_links]), 'unrecognized format for record links'
                    
                    linked_table_name = table_id2name[ field['linked_table_id'] ]
                    for uid in record_links:
                        assert uid in tables[linked_table_name]['records'], 'record id not found in linked table'

# If we've got this far without errors, the integrity is ok.
