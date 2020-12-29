#!/usr/bin/python3
#
# fields.py
#
# Definitions for all the fields in ORM layer
#

# problem statement says there should always be a default
# we force blank to True if default is provided
# otherwise we keep original value of blank
# but if no default is given we always provide a default

from datetime import datetime

def check_elem_type(elem, elem_type):
    if not isinstance(elem, elem_type):
        raise TypeError('elem is wrong type')

def check_choices(choices, elem_type):
    for c in choices:
        if not isinstance(c, elem_type):
            raise TypeError('a choice is the wrong type')

class Integer:   
    def __init__(self, blank=False, default=None, choices=None):
        
        if not choices == None:
            check_choices(choices, int)

        if default == None:
            default = 0
        else: 
            blank = True
            check_elem_type(default, int)
            if not choices == None and not default in choices:
                raise TypeError('default is not in choices')
        
        self.blank = blank
        self.default = default
        self.choices = choices

class Float: 
    def __init__(self, blank=False, default=None, choices=None):
        if not choices == None:
            check_choices(choices, float)

        if default == None:
            default = 0.0
        else: 
            blank = True
            check_elem_type(default, float)
            if not choices == None and not default in choices:
                raise TypeError('default is not in choices')
        
        self.blank = blank
        self.default = default
        self.choices = choices

class String:
    def __init__(self, blank=False, default=None, choices=None):
        if not choices == None:
            check_choices(choices, str)

        if default == None:
            default = ''
        else: 
            blank = True
            check_elem_type(default, str)
            if not choices == None and not default in choices:
                raise TypeError('default is not in choices')
        
        self.blank = blank
        self.default = default
        self.choices = choices
        
class Foreign:
    def __init__(self, table, blank=False):
        self.table = table
        self.blank = blank
    
class DateTime:
    implemented = True

    def __init__(self, blank=False, default=None, choices=None):
        if not choices == None:
            check_choices(choices, datetime)

        if default == None:
            default = datetime.fromtimestamp(0)
        else: 
            blank = True
            if hasattr(default, '__call__'):
                default = default()
            check_elem_type(default, datetime)
            if not choices == None and not default in choices:
                raise TypeError('default is not in choices')
        
        self.blank = blank
        self.default = default
        self.choices = choices

class Coordinate:
    implemented = True

    def __init__(self, blank=False, default=None, choices=None):
        if not choices == None:
            check_choices(choices, tuple)

        if default == None:
            default = (0.0, 0.0)
        else: 
            blank = True
            check_elem_type(default, tuple)
            if not choices == None and not default in choices:
                raise TypeError('default is not in choices')
        
        self.blank = blank
        self.default = default
        self.choices = choices
