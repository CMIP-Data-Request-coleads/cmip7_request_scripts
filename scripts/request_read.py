import os
import json
from pyairtable import Api

## This is a read-only key for the 3 public CMIP7 Fast Track Bases
keyr = 'patp4zreu20JB67zA.c7ae87c7aec8f34081b5773ea936f738eb8b10bf0493a171096064ab9ce163d5'

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
FROMBASE = True
FROMBASE = False

class LoadBase(object):
    """ LoadBase loads bases from air-table into a dictionary object.
    """
    def __init__(self,api):
        self.tables = dict()
        self._tables = dict()
        self.api = api
        self.shadow_table_names = ['tblQcdKgPGU0jFq1b','tbl7L210y9LFpFI7b']

    def load(self,x):

      base = self.api.base(x.id)
      for t in base.tables():
         print ( 'Reading ',x.name,t.name )
         r_list = dict()
         for record in t.all():
             r_list[record['id']] = record['fields'] 
         if t.id in self.shadow_table_names:
             this_name = '__%s__' % t.name
             shadow = True
             print ( 'Shadow ',x.name,t.name )
         else:
             shadow = False
             this_name = t.name
         self.tables[this_name] = (t.id, t.name, x.id, x.name, r_list)

class ReloadBase(object):
    def __init__(self):
        pass

    def load(self,filename):
      j = open( filename, 'r' )
      self.tables = json.load( j )

def from_base():
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
  

if FROMBASE:
    lb = from_base()
else:
    lb = load_json()

tables = lb.tables
