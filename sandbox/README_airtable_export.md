This README explains how to export the Airtable content to json, and what's in the export.
If you only care about **using** the export and don't need to generate it, skip ahead to the **Structure** section.

## How to export the Airtable data request content

An airtable "raw export" to a json file is done by the script `airtable_export.py`.
It can be run at the command-line to export to a specified filename:
```
./airtable_export.py -t my_token_file -f dreq_raw_export.json
```
Or, if the filename is omitted:
```
./airtable_export.py -t my_token_file
```
will write to a default filename containing a timestamp, example: `dreq_raw_export_2024-09-25_04h09m51sUTC.json`. 
This could be useful for archiving.
However the versioned json file in the public "data request content" repo should use one filename consistently, such as `dreq_raw_export.json`, so that subsequent versions update this file and git tracks these updates.
(Otherwise the repo could get bloated with redundant copies, and as of 25 Sep 2024 the json file is about 20 MB.)

Running the script requires a python environment containing the `pyairtable` module, for example:
```
conda create -n my_dreq_env ipython
pip install pyairtable
```
and then `conda activate my_dreq_env` followed by running `airtable_export.py` (the env name is arbitrary).

A text file containing your Airtable token is necessary, which is `my_token_file` in the above example.
The token needs to be generated by signing into Airtable and specifying which bases are accessible via the token, as explained next.


### Generating an Airtable token

Airtable tokens are not supposed to be shared, so if you want to export you should generate your own.
In your web browser, sign into Airtable and go to

https://airtable.com/create/tokens

and click the "Create new token" button.
The "Scopes" and "Access" for the token need to be added.
Some explanation of these is [given here](https://airtable.com/developers/web/api/scopes).
The scopes you add should just give read permission:
```
data.records:read
See the data in records

schema.bases:read
See the structure of a base, like table names or field types
```
"Access" controls which bases are accessible via the token.
The normal choice for the working version of the data request content are the public bases (you probably have to scroll down to find them in the list of bases)
:
```
Data Request Opportunities (Public)
Data Request Physical Parameters (Public)
Data Request Variables (Public)
```
Then hit "Create token". 
Cut-paste your token into a text file (which `airtable_export.py` will take as its `-t` argument), which can include comments to say what it is, for example:
```
# Read-only key for these CMIP7 data request bases: 
#   Opportunities (public view)
#   Variables (public view)
#   Physical Parameters (public view)

pat635xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
replacing the "pat635xx..." string with your token,  which is a long string of random characters.


## Structure of the exported content

The json file basic structure is:
```
{
    'base name 1' : {
        'table name 1' : {
            ...
            'records' : { # dict to contain all records (rows) in the table, indexed by each record's unique id string
                record id 1 : {record info}
                record id 2 : {record info}
                ...
            },
            'fields' : { # dict to contain schema info about the fields found in each record
                field id 1 : {field info}
                field id 2 : {field info}
                ...
            },
        'table name 2' : {...}
        ...
        }
    }
    'base name 2' : {...}
    ...
}
```
For example:
```json
{
  "Data Request Opportunities (Public)": {
    "Comment": {
      "base_id": "appbrFryP1MhstOS3",
      "base_name": "Data Request Opportunities (Public)",
      "id": "tblQqiAzywOppDNvj",
      "name": "Comment",      
      "description": "",
      "fields": {
        "fld5PnZpNhaifVJ8z": {
          "description": "Comment Title",
          "name": "Comment Title",
          "type": "singleLineText"
        },
        "fldKYZsaRAapA58NG": {
          "description": "Variable groups relevant to the comment.",
          "linked_table_id": "tbl4x1RxPwKRZ0VXY",
          "name": "Variable Groups",
          "type": "multipleRecordLinks"
        }, 
    ... 
      "records": {
        "rec5E9oBVZsxdxHKN": {
          "Comment": "The reference to Omon.sltbasin (Omon.slftbasin) is wrong and must be changed to Omon.sltbasin.\n",
          "Comment Title": "Update description",
          "Opportunities": [
            "reczXng420cBQ08hg"
          ],
          "Status": "Done",
          "Theme": [
            "Ocean & Sea-Ice"
          ],
          "Variable Groups": [
            "recPohW0nDzLULHye"
          ]
        },
        ...
```

Each base is a separate top-level entry ("base" is Airtable's term for database).
This is necessary to ensure the integrity of links between different tables in each base.
They are self-consistent within a base, but not across different bases.
Links from a record to one or more other records in other tables appear as lists of record id strings.
In the above example, "Opportunities" and "Variable Groups" are both links (in this instance the lists have length = 1).
The field description indicates which table a link points to, which in the above example for "Variable Groups" is the table with the id string given by `linked_table_id`.
(In this instance it's obvious which table is linked to because the field name is the same as the table name, but that's not required and isn't always the case.)

The script `integrity_check.py` some simple sanity checks on the links, and uniqueness of Compound Names.
