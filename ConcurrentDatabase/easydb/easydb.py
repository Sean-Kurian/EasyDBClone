#!/usr/bin/python3
#
# easydb.py
#
# Definition for the Database class in EasyDB client
#

import socket
import struct
from .exception import *
from .packet import *

def check_table_name(name):
    if not isinstance(name, str):
        raise TypeError('table name is not a string')

    if not name[0].isalpha():
        raise ValueError('table name does nor begin with letter')

    for c in name:
        if not c.isalpha() and not c.isdigit() and not c == '_':
            raise ValueError('table name contains illegal character')

def check_col_name(name):
    if not isinstance(name, str):
        raise TypeError('column name is not a string')

    if not name[0].isalpha():
        raise ValueError('column name does nor begin with letter')

    for c in name:
        if not c.isalpha() and not c.isdigit() and not c == '_':
            raise ValueError('column name contains illegal character')

    if name == 'id':
        raise ValueError('column name cannot be id')

def check_col_type(ctype):
    if not ctype is int and \
        not ctype is str and \
        not ctype is float and \
        not isinstance(ctype, str):

        raise ValueError('illegal column type')

def check_cycle(tables, tbNameDict):
    for table in tables:
        tbName = table[0]
        tbCols = table[1]
        curri = tbNameDict.get(tbName)

        for col in tbCols:
            colType = col[1]
            if isinstance(colType, str):
                if tbNameDict.get(colType) >= curri:
                    raise IntegrityError('circular or out of order ref')

def pack_one_value(value, valueType):
    structType = NULL
    structSize = 0
    structBuf = b''

    if isinstance(valueType, str) or valueType == FOREIGN:  # foreign key
        if not isinstance(value, int):
            raise PacketError('value is wrong type')

        structType = FOREIGN
        structSize = 8
        structBuf = struct.pack('>q', value)

    elif valueType == int:
        if not isinstance(value, int):
            raise PacketError('value is wrong type')

        structType = INTEGER
        structSize = 8
        structBuf = struct.pack('>q', value)

    elif valueType == float:
        if not isinstance(value, float):
            raise PacketError('value is wrong type')

        structType = FLOAT 
        structSize = 8
        structBuf = struct.pack('>d', value)

    elif valueType == str:
        if not isinstance(value, str):
            raise PacketError('value is wrong type')

        structType = STRING
        if len(value) % 4 == 0:
            padded = len(value)
        else: 
            padded = (len(value) // 4 + 1) * 4

        structSize = padded
        structBuf = value.encode('ascii') + b'\0' * (padded - len(value))

    result = struct.pack('>ii', structType, structSize) + structBuf
    return result


class Database:

    def __repr__(self):
        return "<EasyDB Database object>"

    def __init__(self, tables):

        # initialize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.schema = tables
        self.tbNameDict = {}
        self.tbColDict = {}

        # enumerate() will raise TypeError if tb is not iterable
        for tablei, table in enumerate(tables):
            tbName = table[0]
            check_table_name(tbName)

            if tbName in self.tbNameDict:
                raise ValueError('table name already exists')
            self.tbNameDict[tbName] = tablei
            self.tbColDict[tbName] = {}

            for coli, col in enumerate(table[1]):
                colName = col[0]
                check_col_name(colName)

                if colName in self.tbColDict[tbName]:
                    raise ValueError('column name already exists')
                self.tbColDict[tbName][colName] = coli

                colType = col[1]

        # must check this after as you can use tables declared later
        for table in iter(tables):
            for col in iter(table[1]):
                colType = col[1]
                check_col_type(colType)

                if isinstance(colType, str) and not colType in self.tbNameDict:
                    raise IntegrityError('foreign key to non-existent table')

        check_cycle(tables, self.tbNameDict)

    def connect(self, host, port):
        # connect to the database
        self.sock.connect((host, int(port)))

        # receive response
        resp = self.sock.recv(4096)
        iresp = struct.unpack('>i', resp)[0]

        # check response
        if iresp == OK:
            return True

        if iresp == SERVER_BUSY:
            self.sock.close()

        return False

    def close(self):
        exitReq = struct.pack('>ii', EXIT, 1)
        self.sock.send(exitReq)
        self.sock.close()

    def insert(self, table_name, values):
        if not isinstance(table_name, str) or not table_name in self.tbNameDict:
            raise PacketError('invalid table name')

        # request struct
        command = INSERT
        tableId = self.tbNameDict.get(table_name)
        request = struct.pack('>ii', command, tableId + 1)

        # row struct
        sendStruct = request + struct.pack('>i', len(values))

        table = self.schema[tableId]
        tableCols = table[1]

        if not len(values) == len(tableCols):
            raise PacketError('row has wrong number of elements')

        for i, value in enumerate(values):
            sendStruct = sendStruct + pack_one_value(value, tableCols[i][1])

        resMode = -1
        resKey = -1
        resVersion = -1
        while resMode != OK:
            self.sock.send(sendStruct)
            res = self.sock.recv(4096)
            resMode = struct.unpack('>i', res[:4])[0]

            if resMode == NOT_FOUND:
                raise ObjectDoesNotExist

            if resMode == BAD_FOREIGN:
                raise InvalidReference

            if resMode == TXN_ABORT:
                raise TransactionAbort

            if not resMode == OK:
                continue

            resKey = struct.unpack('>q', res[4:12])[0]
            resVersion = struct.unpack('>q', res[12:])[0]

        return (resKey, resVersion)

    def update(self, table_name, pk, values, version=None):
        # request struct
        command = UPDATE
        tableId = self.tbNameDict.get(table_name)
        request = struct.pack('>ii', command, tableId + 1)

        # key struct
        if not isinstance(pk, int):
            raise PacketError('row id is not an integer')
        if not version is None and not isinstance(version, int):
            raise PacketError('version is not an integer')

        if version is None:
            version = 0
        key = struct.pack('>qq', pk, version)

        # row struct
        sendStruct = request + key + struct.pack('>i', len(values))

        table = self.schema[tableId]
        tableCols = table[1]

        for i, value in enumerate(values):
            sendStruct = sendStruct + pack_one_value(value, tableCols[i][1])

        resMode = -1
        while resMode != OK:
            self.sock.send(sendStruct)
            res = self.sock.recv(4096)
            resMode = struct.unpack('>i', res[:4])[0]

            if resMode == NOT_FOUND:
                raise ObjectDoesNotExist

            if resMode == BAD_FOREIGN:
                raise InvalidReference

            if resMode == TXN_ABORT:
                raise TransactionAbort

            if not resMode == OK:
                continue

            resVersion = struct.unpack('>q', res[4:])[0]

        return resVersion

    def drop(self, table_name, pk):

        tableExists = False

        if isinstance(pk, int):
            for tb in enumerate(self.tbNameDict):
                if (tb[1] == table_name):
                     dropCmd = struct.pack('>ii',DROP,tb[0]+1)
                     tableExists = True
                     break
        else:
            raise PacketError('pk is not an integer')



        if (not tableExists):
            raise PacketError('table does not exist')

        #pack and send bytes
        idNum = struct.pack('>q', pk)
        dropReq = dropCmd + idNum
        self.sock.send(dropReq)

        # receive response
        resp = self.sock.recv(4096)
        iresp = struct.unpack('>i', resp)[0]

        # check response
        if iresp == OK:
            return True

        if iresp == NOT_FOUND:
            raise ObjectDoesNotExist('specified row could not be found')

    def get(self, table_name, pk):
        tableExists = False
        elType, elSize, row_list = ([] for i in range(3))

        if isinstance(pk, int):
            for tb in enumerate(self.tbNameDict):
                if (tb[1] == table_name):
                     getCmd = struct.pack('>ii',GET,tb[0]+1)
                     tableExists = True
                     break
        else:
            raise PacketError('pk is not an integer')


        if (not tableExists):
            raise PacketError('table doesn\'t exist')

        #pack and send bytes
        idNum = struct.pack('>q', pk)
        getReq = getCmd + idNum
        self.sock.send(getReq)

        # receive response
        resp = self.sock.recv(4096)

        # check response
        iresp = struct.unpack('>i', resp[:4])[0]
        
        if (iresp == NOT_FOUND): 
            raise ObjectDoesNotExist('table index does not exist')
        
        if (len(resp) > 4): 
            data = resp[16:]
            rowSize = struct.unpack('>i', resp[12:16])[0]
            ver = struct.unpack('>q', resp[4:12])[0]

            for i in range(rowSize): 
                elType.append(struct.unpack('>i', data[:4])[0])
                elSize.append(struct.unpack('>i', data[4:8])[0])
                data = data[8:]
                 
                # unpack by element type

                if(elType[i] == STRING): 
                    unpackStr = (struct.unpack(('>' + str(elSize[i]) + 's'), data[:elSize[i]])[0]).decode()
                    row_list.append(unpackStr.replace('\x00',''))
                if(elType[i] == INTEGER or elType[i] == FOREIGN):
                    row_list.append(struct.unpack('>q', data[:elSize[i]])[0])
                if(elType[i] == FLOAT): 
                    row_list.append(struct.unpack('>d', data[:elSize[i]])[0])  
                data = data[elSize[i]:]

        return (row_list, ver)

    def scan(self, table_name, op, column_name=None, value=None):
        command = SCAN

        # table id
        try:
            tableId = self.tbNameDict[table_name]
        except KeyError:
            raise PacketError('table with name does not exist')

        # operator
        if not (op == operator.AL or op == operator.EQ or op == operator.NE or \
                op == operator.LT or op == operator.GT):

            raise PacketError('illegal operator')

        # column id
        colId = -1  # 0 will be sent to the db: id col
        if op != operator.AL:
            try:
                colId = self.tbColDict[table_name][column_name]
            except KeyError:
                if column_name != 'id':
                    raise PacketError('column not found')

        # column value type
        if column_name == 'id':
            colType = FOREIGN
        else:
            colType = self.schema[tableId][1][colId][1]

        if op != operator.AL: 
            if colType == int or colType == str or colType == float:
                if not isinstance(value, colType):
                    raise PacketError('value is wrong type non-foreign')

            if isinstance(colType, str) or colType == FOREIGN:
                if not isinstance(value, int):
                    raise PacketError('value is wrong type foreign')

                if op != operator.EQ and op != operator.NE:
                    raise PacketError('foreign key only supports EQ and NE')

        # send request
        request = struct.pack('>ii', command, tableId + 1)
        colOp = struct.pack('>ii', colId + 1, op)

        if op == operator.AL:
            packed_value = struct.pack('>ii', NULL, 0)
        else:
            packed_value = pack_one_value(value, colType)

        self.sock.send(request + colOp + packed_value)

        # receive response
        resp = self.sock.recv(4096)
        code = struct.unpack('>i', resp[:4])[0]
        resp = resp[4:]

        count = struct.unpack('>i', resp[:4])[0]
        resp = resp[4:]

        # unpack ids
        foundList = []
        for i in range(count):
            id = struct.unpack('>q', resp[:8])[0]
            resp = resp[8:]
            foundList.append(id)

        return foundList

