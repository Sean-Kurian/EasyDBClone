#!/usr/bin/python3
#
# orm.py
#
# Definition for setup and export function
#

from .easydb import Database
from datetime import datetime
from .field import *

def get_tables_tuple(database_name, module):
    db = []
    # create the tables based on the schema classes
    for mem in module.__dict__:
        if not mem[0] == '_' and not mem == 'orm' and not mem == 'datetime':
            fields = []
            for attr in module.__dict__[mem].__dict__:
                if not attr[0] == '_':
                    field_type = module.__dict__[mem].__dict__[attr]

                    if isinstance(field_type, Integer):
                        fields.append( (attr, int) )

                    elif isinstance(field_type, String):
                        fields.append( (attr, str) )

                    elif isinstance(field_type, Float):
                        fields.append( (attr, float) )

                    elif isinstance(field_type, Foreign):
                        fields.append( (attr, field_type.table.__name__) )

                    elif isinstance(field_type, DateTime):
                        fields.append( (attr, float) )

                    elif isinstance(field_type, Coordinate):
                        fields.append( (attr + '_x', float) )
                        fields.append( (attr + '_y', float) )

                    else:
                        raise AttributeError(field_type, "is unrecognized type")
            db.append( (mem, tuple(fields)) )
    return tuple(db)

# Return a database object that is initialized, but not yet connected.
#   database_name: str, database name
#   module: module, the module that contains the schema
def setup(database_name, module):
    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))

    db = get_tables_tuple(database_name, module)
    return Database(db) 

# Return a string which can be read by the underlying database to create the 
# corresponding database tables.
#   database_name: str, database name
#   module: module, the module that contains the schema
def export(database_name, module):

    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))

    typestrs = {
        str: 'string',
        int: 'integer',
        float: 'float'
    }
    db = get_tables_tuple(database_name, module)
    ret = ''
    for table in db:
        ret += table[0] + ' { '
        for attr in table[1]:
            if attr[1] in typestrs:
                ret += attr[0] + ' : ' + typestrs[attr[1]] + ' ; '
            else: ret += attr[0] + ' : ' + attr[1] + ' ; '
        ret += '} '
    return ret

