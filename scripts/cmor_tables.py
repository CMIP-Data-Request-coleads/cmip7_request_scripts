
import json
import request_read
import request_classes

lb = request_read.load_json()
dr = request_classes.import_request()

class CMOR_Variable(object):
    __fails__ = []
    def __init__(self,record):
        self.d = record.__dict__
        self.o = dict()
        self.vid = self.d.get('compound_name','')
        self.status = self.d.get('status','')
        if self.vid == '':
            print ('EMPTY compound_name', self.d.get('status','--'))
            self.__fails__.append( ('EMPTY compound_name', self.d.get('status','--')) )
        else:
            self.get_physical_parameter()
            self.get_cell_methods()
            self.get_title()
        print( self.vid, self.status, self.o )

    def get_cell_methods(self):
        try:
          x = self.d.get('cell_methods','')
        except:
          print( self.vid,'FAILED to get cell methods' )
          print( self.d.keys() )
        if x == '':
          self.o['cell_methods'] = x
        else: 
            try:
               self.o['cell_methods'] = x[0].cell_methods
            except:
                print( self.vid, x[0].__dict__.keys() )
                self.__fails__.append( ('NO CELL METHODS', self.vid) )

    def get_title(self):
        try:
          x = self.d.get('title','')
        except:
          print( 'FAILED to get title' )
          print( self.d.keys() )
          self.__fails__.append( ('NO TITLE', self.vid) )
        if x == '':
          print( 'EMPTY title' )
        self.o['title'] = x

    def get_physical_parameter(self):
        try:
          x = self.d.get('physical_parameter','')
        except:
          print( 'FAILED to get physical parameter' )
          print( self.d.keys() )
        if x == '':
          self.o['physical_parameter'] = x
        else: 
          try:
            self.o['physical_parameter'] = x[0].name
          except:
            print( self.vid, x[0] )
            raise


l1 = []
for r in dr.variables.record_list:
  this = CMOR_Variable( r )

  ##assert type(ee['cell_methods']) == type(''),'%s  -- %s' % (r.compound_name, r.title)
  ##l1.append(ee)

print (CMOR_Variable.__fails__)


##oo = open( 'mip_tables_alphaalpha', 'w' )
##oo.write( json.dumps( dict( data=l1) , sort_keys=True, indent=4) )
##oo.close()

