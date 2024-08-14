import os
import json
from pyairtable import Api


## Initial Structure [[ not exactly what is implemented below ]]
##
##  base[<base name>] = dict( id->str, table->dict )
##  table[<table name>] = dict( id->str, fields->dict, records->list )
##  records[x] = dict( id->str, record->dict )
##
##  Hence, the folowing is the list of records in the Variables table.
##
##  vars = base['Data Request Variables (Public)']['table']['Variables']['records']
##
##
FROMBASE = False
FROMBASE = True

def nstr(xx):
    if xx == None:
        return ''
    else:
        return str(xx)


class LoadBase(object):
    """ LoadBase loads bases from air-table into a dictionary object.
    """
    def __init__(self,api):
        self.tables = dict()
        self.table_objs = dict()
        self._tables = dict()
        self.api = api
        ## shadow_table_names is used to identify synced tables so that mappings from one base to another can be tracked.
        ## manually copied for air table.
        self.shadow_table_names = ['tblQcdKgPGU0jFq1b','tbl7L210y9LFpFI7b']

    def load(self,x):

      base = self.api.base(x.id)
      for t in base.tables():
         print ( 'Reading ',x.name,t.name )
         r_list = dict()
         s=t.schema()
         for record in t.all():
             r_list[record['id']] = record['fields'] 
         if t.id in self.shadow_table_names:
             this_name = '__%s__' % t.name
             shadow = True
             print ( 'Shadow ',x.name,t.name )
         else:
             shadow = False
             this_name = t.name
         self.tables[this_name] = dict(id=t.id, name=t.name, description=nstr(s.description), base_id=x.id, base_name=x.name, records=r_list)

         self.table_objs[this_name] = t

class ReloadBase(object):
    def __init__(self):
        pass

    def load(self,filename):
      j = open( filename, 'r' )
      self.tables = json.load( j )

def from_base():
## This is a read-only key for the 3 public CMIP7 Fast Track Bases
## keys are private. If you have a user account, see https://airtable.com/create/tokens
  keyr = open( '/home/mjuckes/Repositories/airtable_read_key' ).readlines()[0].strip()

  api = Api(keyr)
  lb = LoadBase(api)

  for x in api.bases():
      lb.load(x)

  j = open( 'request_basic_dump2.json', 'w' )
  j.write( json.dumps(lb.tables, sort_keys=True, indent=4))
  j.close()
  return lb

def load_json():
  lb = ReloadBase()
  lb.load('request_basic_dump2.json')
  return lb
  

if __name__ == "__main__":

  if FROMBASE:
    lb = from_base()
  else:
    lb = load_json()

  tables = lb.tables
