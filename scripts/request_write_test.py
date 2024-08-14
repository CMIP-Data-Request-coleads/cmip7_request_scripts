
import request_read as rr


## note that read fails if schema read is not enabled.

key = open( '/home/mjuckes/Repositories/sandpit_variable_views_write' ).readlines()[1].strip()

api = rr.Api(key)
lb = rr.LoadBase(api)

x = api.bases()[0]
lb.load(x)


