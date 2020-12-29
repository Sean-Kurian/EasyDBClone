#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#
from .field import *
from datetime import datetime
from .easydb import operator, IntegrityError, InvalidReference, ObjectDoesNotExist, \
    TransactionAbort, PacketError
import orm 
import collections


# metaclass of table
# Implement me or change me. (e.g. use class decorator instead)
class MetaTable(type):
    types = [Integer, Float, String, Foreign, DateTime, Coordinate]
    reserved_names = ['pk', 'version', 'save', 'delete']
    created_names = set()

    @classmethod    # from lecture slides "lec10-1", slide 16
    def __prepare__(mcs, name, bases, **kwargs):
        return collections.OrderedDict()

    def __init__(cls, name, bases, attrs):
        if name in cls.created_names:
            raise AttributeError('table name already exists')
        cls.created_names.add(name)
        
        for attr in attrs:
            if type(attrs[attr]) in cls.types:
                if attr in cls.reserved_names:
                    raise AttributeError('cannot name column after keyword')
                if '_' in attr:
                    raise AttributeError('column name cannot contain underscore')

        
    # Returns an existing object from the table, if it exists.
    #   db: database object, the database to get the object from
    #   pk: int, primary key (ID)
    def get(cls, db, pk):

        values, version = db.get(cls.__name__, pk)

        namelist = []
        for item in cls.__dict__.values():
            for x in cls.__class__.__dict__['types']:
                if isinstance(item, x): 
                    namelist.append(item)

        attrlist = []
        for item in cls.__dict__:
            if item.startswith('__') == False:
                attrlist.append(item)
        
        columns = {}
        for typei in range(len(namelist)):
            typeobj = namelist[typei]
            colname = attrlist[typei]
            
            if (isinstance(typeobj, Foreign)): 
                columns[colname] = typeobj.table.get(db, values[typei])

            elif isinstance(typeobj, Coordinate):
                columns[colname] = (values[typei], values[typei+1])
                del values[typei]

            elif isinstance(typeobj, DateTime):
                columns[colname] = datetime.utcfromtimestamp(values[typei])
                
            else: 
                columns[colname] = values[typei]
        
        obj = cls(db, **columns)
        obj.pk = pk

        return obj

    # Returns a list of objects that matches the query. If no argument is given,
    # returns all objects in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def filter(cls, db, **kwarg):
        found_ids = []

        if len(kwarg) == 0:
            found_ids = db.scan(cls.__name__, operator.AL)
        else:
            key, value = 0, 0   # values will never be used
            for k in kwarg: # there should only be one item
                key = k
                value = kwarg[k]
            if isinstance(value, Table):
                value = value.pk
            
            tokens = key.split('__')
            typeobj = cls.__dict__[tokens[0]]

            if len(tokens) == 1: # eq sign only
                if isinstance(typeobj, Coordinate):
                    found_idsx = db.scan(cls.__name__, operator.EQ, tokens[0]+'_x', value[0])
                    found_idsy = db.scan(cls.__name__, operator.EQ, tokens[0]+'_y', value[1])
                    for i in found_idsx:
                        if i in found_idsy:
                            found_ids.append(i)
                else:
                    found_ids = db.scan(cls.__name__, operator.EQ, tokens[0], value)
            else:
                op = tokens[1]
                
                # special treatment
                if isinstance(typeobj, Coordinate):
                    if op == 'ne':
                        found_idsx = db.scan(cls.__name__, operator.NE, tokens[0]+'_x', value[0])
                        found_idsy = db.scan(cls.__name__, operator.NE, tokens[0]+'_y', value[1])
                        found_ids = list(set(found_idsx.append(found_idsy)))
                    
                    elif op == 'gt':
                        found_idsx = db.scan(cls.__name__, operator.GT, tokens[0]+'_x', value[0])
                        found_idsy = db.scan(cls.__name__, operator.GT, tokens[0]+'_y', value[1])
                        for i in found_idsx:
                            if i in found_idsy:
                                found_ids.append(i)

                    elif op == 'lt':
                        found_idsx = db.scan(cls.__name__, operator.LT, tokens[0]+'_x', value[0])
                        found_idsy = db.scan(cls.__name__, operator.LT, tokens[0]+'_y', value[1])
                        
                        for i in found_idsx:
                            if i in found_idsy:
                                found_ids.append(i)
                    else:
                        raise AttributeError('invalid operator for Coordinate')
                else:
                    # other operators
                    if op == 'ne':
                        found_ids = db.scan(cls.__name__, operator.NE, tokens[0], value)
                    elif op == 'gt':
                        found_ids = db.scan(cls.__name__, operator.GT, tokens[0], value)
                    elif op == 'lt':
                        found_ids = db.scan(cls.__name__, operator.LT, tokens[0], value)
                    else:
                        raise AttributeError('unknown operator')

        return [cls.get(db, i) for i in found_ids]


    # Returns the number of matches given the query. If no argument is given, 
    # return the number of rows in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def count(cls, db, **kwarg):

        if len(kwarg) == 0:  
            return len(list(db.scan(cls.__name__, operator.AL))) 
        for val, col in kwarg.items(): 
            if '__' in val: 
                colname = val.replace("__" + val[len(val)-2:],"")
                if colname not in cls.__dict__ and colname != 'id': 
                    raise AttributeError('not listed in schema')
                if val[len(val)-2:] == 'ne': 
                    return len(list(db.scan(cls.__name__, operator.NE, colname, col)))
                elif val[len(val)-2:] == 'lt': 
                    return len(list(db.scan(cls.__name__, operator.LT, colname, col)))
                elif val[len(val)-2:] == 'gt':               
                    return len(list(db.scan(cls.__name__, operator.GT, colname, col))) 
                else: 
                    raise AttributeError('operator not supported')
            else: 
                if type(col) == int: 
                    return len(list(db.scan(cls.__name__, 2, val, col))) 
                raise PacketError
        return list()

# check that the given value is appropriate for the column type object
def check_type_value(type_obj, val):
    if not isinstance(type_obj, Foreign) and type_obj.choices != None:
        if not val in type_obj.choices:
            raise ValueError('value not a valid choice')
        
    else:
        if isinstance(type_obj, Integer):
            if not isinstance(val, int):
                raise TypeError('value is not an int')

        elif isinstance(type_obj, Float):
            if isinstance(val, int):
                val = float(val)
            if not isinstance(val, float):
                raise TypeError('value is not a float')

        elif isinstance(type_obj, String):
            if not isinstance(val, str):
                raise TypeError('value is not a string')

        elif isinstance(type_obj, Foreign):
            if not isinstance(val, type_obj.table):
                raise TypeError('value is not right type of foreign')

        elif isinstance(type_obj, DateTime): #check timestamp values
            if not isinstance(val, datetime):
                raise TypeError('value is not datetime')

        elif isinstance(type_obj, Coordinate):
            if not isinstance(val, tuple) or not len(val) == 2: #for coordinate, check latitude and longitude
                raise TypeError('value is not a tuple')

            
            if not isinstance(val[0], int) and \
                not isinstance(val[0], float) or \
                not isinstance(val[1], int) and \
                not isinstance(val[1], float):

                raise TypeError('coordinates are not floats')

            if val[0] < -90 or val[0] > 90 or \
                val[1] < -180 or val[1] > 180:

                raise ValueError('coordinates out of bounds')

# table class
# Implement me.
class Table(object, metaclass=MetaTable):
    def __setattr__(self, field_name, val):
        try:
            type_obj = self.__class__.__dict__[field_name]
        except KeyError:    # not a database field
            self.__dict__[field_name] = val
            return
        
        if not type(type_obj) in MetaTable.types:   # not a database field
            self.__dict__[field_name] = val
            return

        if val == None: # database field with no value given
            if type_obj.blank == True:
                if isinstance(type_obj, Foreign):
                    self.__dict__[field_name] = None
                else:
                    self.__dict__[field_name] = type_obj.default
            else:
                raise AttributeError('missing required attribute')

        else:   # database field with value given
            check_type_value(type_obj, val)

            # special case where int gets parsed into float
            if isinstance(type_obj, Float) and isinstance(val, int):
                val = float(val)

            self.__dict__[field_name] = val
        
    # initialize the table
    def __init__(self, db, **kwargs):
        self.pk = None      # id (primary key)
        self.version = None # version
        self._db = db
        
        # go through all of the class fields
        for field_name in self.__class__.__dict__:
            if not field_name in kwargs:
                setattr(self, field_name, None)
            else:
                setattr(self, field_name, kwargs[field_name])

    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        table_name = str(self).split(':')[0].split('<')[1]
        
        values = []
        keylist = []

        for key in self.__dict__.keys(): 
            if not key.startswith('_') and not key == 'pk' and not key == 'version': 
                type_obj = self.__class__.__dict__[key]
                
                if isinstance(type_obj, Coordinate):
                    values.append(self.__dict__[key][0])
                    keylist.append(key + '_x')
                    values.append(self.__dict__[key][1])
                    keylist.append(key + '_y')

                elif isinstance(type_obj, DateTime):
                    keylist.append(key)
                    values.append(self.__dict__[key].timestamp())
                    
                else: 
                    values.append(self.__dict__[key])
                    keylist.append(key)
        
        if self.pk is not None: 
            if atomic is False: 
                self.version = self._db.update(table_name, self.pk, values, version = 0)
            else:
                try:  
                    for key, field in zip(self.__class__.__dict__.keys(), self.__class__.__dict__.values()): 
                        if key in keylist: 
                            if isinstance(field, Foreign): 
                                value = getattr(self, key) 
                                if isinstance(value, int): 
                                    pass
                                elif value.pk is None: 
                                    value.save()
                                    values[0] = value.pk
                                elif value.pk is not None: 
                                    values[0] = value.pk
                                else: 
                                    raise InvalidReference('ref not valid')
                    self.version = self._db.update(table_name, self.pk, values, self.version)
                except PacketError: 
                    raise InvalidReference('reference is not valid2')
        else: 
            for key, field in zip(self.__class__.__dict__.keys(), self.__class__.__dict__.values()): 
                if key in keylist: 
                    if isinstance(field, Foreign): 
                        value = getattr(self, key) 
                        
                        if value.pk is None: 
                            value.save()
                            values[0] = value.pk
                        else: 
                            raise InvalidReference('reference is not valid')
            self.pk, self.version = self._db.insert(table_name, values)


        
    # Delete the row from the database.
    def delete(self):
        table_name = str(self).split(':')[0].split('<')[1]
        self._db.drop(table_name, self.pk)
        self.pk = None
        self.version = None

