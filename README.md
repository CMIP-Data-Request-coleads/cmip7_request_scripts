# CMIP7 Data Request Scripts
A collection of scripts for the CMIP7 fast track data request.

THESE SCRIPTS ARE PROVIDED TO ILLUSTRATE IMPLEMENTATION OF BASIC TASKS. THERE IS NO ONGOING SUPPORT.

`request_read.py` : Reads the full contents of the public bases and dumps contents to a JSON file, or reads in the JSON file. JSON file format mirrors Air Table format closely and is not human friendly. Links between records are indicated by opaque record identifiers. This JSON file is approximately 218k records at present. To read from Air Table a personal access token is needed. This requires an account, and availability is limited to participants Data Request management.

`request_classes.py` : Loads request contents into a set of classes for Tables and Records, and converts links between records to direct references. 

`request_write_test.py` : Tests the `pyairtable` write API [personal access token needed].

Usage: 
```
import request_classes as rc
b = rc.import_request()
```
Dependecies: The script uses `request_read`.

Thus `t = b.tables['Opportunity']` is the Opportunity table, with description `t.description`.

 * r = r.record_list[1] is a record and r.variable_groups is a list of variable groups.
 * v = r.variable_groups[0].variables[0] is a variable
