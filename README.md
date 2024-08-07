# cmip7_scripts
A collection of scripts for the CMIP7 fast track data request



`request_read.py` : Reads the full contents of the public bases and dumps contents to a JSON file, or reads in the JSON file. JSON file format mirrors Air Table format closely and is not human friendly. Links between records are indicated by opaque record identifiers.

`request_classes.py` : Loads request contents into a set of classes for Tables and Records, and converts links between records to direct references. 
