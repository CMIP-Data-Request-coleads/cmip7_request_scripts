
import json
import request_read
import request_classes
import collections

lb = request_read.load_json()
dr = request_classes.import_request()

class CMOR_Variable(object):
    __fails__ = []
    def __init__(self,record):
        self.d = record.__dict__
        self.o = dict()
        self.vid = self.d.get('compound_name','')
        self.status = self.d.get('status','')
        self._rv = 0
        if self.status == 'CMIP6 CMOR variable':
          if self.vid == '':
            print ('EMPTY compound_name', self.d.get('status','--'))
            self.__fails__.append( ('EMPTY compound_name', self.d.get('status','--')) )
            self._rv = 0
          else:
            self.get_physical_parameter()
            self.get_cell_methods()
            self.get_cell_measures()
            self.get_misc()
            self.get_comment()
            self.get_title()
            self._rv = 1
        print( self.vid, self.status, self.o )

    def MIP_table_dict(self):
        return {k:self.o[k] for k in self.o.keys() - {'table',}}

    def get_cell_methods(self):
        try:
          x = self.d.get('cell_methods','')
        except:
          print( self.vid,'FAILED to get cell methods' )
          print( self.d.keys() )
          self._rv = 0
        if x == '':
          self.o['cell_methods'] = x
        else: 
            try:
               self.o['cell_methods'] = x[0].cell_methods
            except:
                print( self.vid, x[0].__dict__.keys() )
                self.__fails__.append( ('NO CELL METHODS', self.vid) )
                self._rv = 0

    def get_cell_measures(self):
        try:
          x = self.d.get('cell_measures','')
        except:
          print( self.vid,'FAILED to get cell measures' )
          print( self.d.keys() )
          self._rv = 0
        if x == '':
          self.o['cell_measures'] = x
        else: 
            try:
               self.o['cell_measures'] = x[0].name
            except:
                print( self.vid, x[0].__dict__.keys() )
                self.__fails__.append( ('NO CELL MEASURES', self.vid) )
                self._rv = 0

    def get_title(self):
        try:
          x = self.d.get('title','')
        except:
          print( 'FAILED to get title' )
          print( self.d.keys() )
          self._rv = 0
          self.__fails__.append( ('NO TITLE', self.vid) )
        if x == '':
          print( 'EMPTY title' )
        self.o['long_name'] = x

    def get_comment(self):
        try:
          x = self.d.get('description','')
        except:
          print( 'FAILED to get description' )
          print( self.d.keys() )
          self._rv = 0
          self.__fails__.append( ('NO description', self.vid) )

        self.o['comment'] = x

    def get_misc(self):
        for this in ['positive','type','frequency','table']:
          try:
            x = self.d.get(this,'')
          except:
            print( 'FAILED to get %s' % this )
            print( self.d.keys() )
            self.__fails__.append( ('NO %s' % this, self.vid) )
            self._rv = 0
          if type (x) == type( () ):
              x = x[0]
          self.o[this] = x
        self.table = self.o['table']

    def get_title(self):
        try:
          x = self.d.get('title','')
        except:
          print( 'FAILED to get title' )
          print( self.d.keys() )
          self._rv = 0
          self.__fails__.append( ('NO TITLE', self.vid) )
        if x == '':
          print( 'EMPTY title' )
        self.o['long_name'] = x

    def get_physical_parameter(self):
        try:
          x = self.d.get('physical_parameter','')
        except:
          print( 'FAILED to get physical parameter' )
          print( self.d.keys() )
          self._rv = 0
        if x == '':
          self.o['out_name'] = x
        else: 
          try:
            self.o['out_name'] = x[0].name
            self.o['units'] = x[0].units
            self.o['standard_name'] = x[0].cf_standard_name[0].name
          except:
            print( self.vid, x[0] )
            self.__fails__.append( ('FAILED TO LOAD PHYSICAL PARAMETER',self.vid,x[0].id) )


l1 = []

Header= {
    "Conventions": "CF-1.7 CMIP-6.5",
    "approx_interval": 30.0,
    "checksum": "",
    "cmor_version": "3.8.0",
    "data_specs_version": "6.5.0.0",
    "generic_levels": "",
    "int_missing_value": "-999",
    "missing_value": "1e20",
    "product": "model-output",
    "table_date": None,
    "table_id": None,
  }


cc = collections.defaultdict( list )
for r in dr.variables.record_list:
  this = CMOR_Variable( r )
  if this._rv == 1:
    cc[this.table].append( this.MIP_table_dict() )


for k,l in cc.items():
    print ('WRITING',k)
    h = Header.copy()
    h["table_id"] = k
    h["table_date"] = '2nd sep'
    fn = 'out/MIP_%s.json' % k
    variables = {x['out_name']:x for x in l}
    oo = open(fn,'w')
    oo.write( json.dumps( dict( Header=h, variable_entry=variables ),  sort_keys=True, indent=4) )
    oo.close()





  ##assert type(ee['cell_methods']) == type(''),'%s  -- %s' % (r.compound_name, r.title)
  ##l1.append(ee)

print (CMOR_Variable.__fails__)


##oo = open( 'mip_tables_alphaalpha', 'w' )
##oo.write( json.dumps( dict( data=l1) , sort_keys=True, indent=4) )
##oo.close()

