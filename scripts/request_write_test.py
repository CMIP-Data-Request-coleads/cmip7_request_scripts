import request_read as rr
from datetime import date
today = date.today().ctime()

## note that read fails if schema read is not enabled.
## 15th Aug: successfully updates a record. Read of all tables is wasted resource and should be eliminated.

key = open( '/home/mjuckes/Repositories/sandpit_variable_views_write' ).readlines()[1].strip()

api = rr.Api(key)
lb = rr.LoadBase(api)

x = api.bases()[0]
lb.load(x)


t = lb.table_objs['CF standard name import']
t.create( {'Name':today, 'Notes':'Test' } )


