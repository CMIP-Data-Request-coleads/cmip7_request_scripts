import collections


class Request(object):
    software_version = '0.1.0'
    records = dict()
    tables = dict()
    record_by_uid = collections.defaultdict( set )
    record_by_name = collections.defaultdict( set )
    rmap = dict()

class Base(Request):
    def __init__(self):
        pass

def implement():
    for k,i in Request.record_by_name.items():
        if len(i) == 2:
            i0,i1 = list(i)
            Request.rmap[i0.id] = i1.id
            Request.rmap[i1.id] = i0.id

def lscore(xx):
            kk = xx.lower()
            if kk.find(' '):
               kk = '_'.join(kk.split())
            return kk
    
class Record(Request):
    def __init__(self,id,record_dict,shadow):
        self.index = set(['id',])
        for k,i in record_dict.items():
            kk = lscore(k)
            assert kk not in self.__dict__
            self.__dict__[kk] = i
            self.index.add(kk)
        self.id = id
        if not shadow:
          self.records[self.id] = self
        if 'uid' in self.index:
            self.record_by_uid[self.uid].add(self)

    def __info__(self):
        print ( '%s [%r]' % (self.__class__, {k:self.__dict__[k] for k in self.index} ) )

    def __repr__(self):
        if 'name' in self.index:
          return '%s' % self.name
        else:
          return '%s' % (self.__class__)

    def __implement__(self):
        for kk in self.index:
            this = self.__dict__[kk]
            if type( this ) == type('') and this in self.records:
                self.__dict__[kk] = self.records[this]
            elif type( this ) in [type( () ), type( [] )] and all( [type(x) == type('') for x in this] ):
                that = []
                for x in this:
                    if x in self.records:
                        that.append( self.records[x] )
                    elif x in self.rmap:
                        that.append( self.records[self.rmap[x]] )
                    else:
                        that.append( x)
                self.__dict__[kk] = tuple(that)



class Table(Request):
    def __init__(self,name,records,shadow=False):
        self.record_list = []
        self.name_dict = dict()
        Request.tables[name] = self
        for k,r in records.items():
          rec = Record(k,r,shadow)
          self.record_list.append( rec )
          if 'name' in rec.index:
              n = rec.name
          elif 'compound_name' in rec.index:
              n = rec.compound_name
          else:
              n = None
          if n != None:
            self.name_dict[n] = rec
            self.record_by_name[n].add(rec)


    def by_name(self,name):
        return self.name_dict[name]



def import_request():
  import request_read as rr
  b = Base()
  for n,tt in rr.lb.tables.items():
      t = Table(n,tt[-1])
      nn = lscore(n)
      assert nn not in b.__dict__
      b.__dict__[nn] = t
  for n,tt in rr.lb._tables.items():
      t = Table(n,tt[-1],shadow=True)
  implement()
  return b
