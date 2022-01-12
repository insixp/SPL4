from os import stat
import sqlite3
import inspect
from sqlite3.dbapi2 import paramstyle

class DAO:
    def __init__(self, conn, dto_type):
        self._conn = conn
        self._dto_type = dto_type
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_inst):
        inst_dict = vars(dto_inst)
        column_names = ','.join(inst_dict.keys())
        values = list(inst_dict.values())
        q_mark_insert = ','.join('?' * len(values))
        statment = "INSERT INTO {} ({}) VALUES ({})".format(self._table_name, column_names, q_mark_insert)
        try:
            self._conn.execute(statment, values)
            return True
        except BaseException as e:
            print("Error: " + str(e))
            return False

    def find(self, kwargs, order_by=None):
        col_names   = list(kwargs.keys())
        params      = list(kwargs.values())

        if(len(col_names ) == 0):
            statement = "SELECT * FROM {}".format(self._table_name)
        else:
            statement = "SELECT * FROM {} WHERE {}".format(self._table_name, ' AND '.join([col + "=?" for col in col_names]))
        if(order_by != None):
            statement += " ORDER BY {}".format(order_by) 
        cursor = self._conn.cursor()
        try:
            cursor.execute(statement, params)
        except BaseException as e:
            print("Error: " + str(self._dto_type) + " can't find: " + str(e))
            return None
        return orm(cursor, self._dto_type)
    
    def delete(self, **kwargs):
        col_names   = list(kwargs.keys())
        params      = list(kwargs.values())

        if(len(col_names ) == 0):
            statement = "DELETE FROM {}".format(self._table_name)
        else:
            statement = "DELETE FROM {} WHERE {}".format(self._table_name, ' AND '.join([col + "=?" for col in col_names]))
        try:
            self._conn.execute(statement, params)
            return True
        except BaseException as e:
            print("Error: " + self.__name__ + " can't find: " + str(e))
            return False
                
    def update(self, set_values, cond):
        set_col_names   = list(set_values.keys())
        set_params      = list(set_values.values())
        cond_col_names  = list(cond.keys())
        cond_params     = list(cond.values())
        statement = 'UPDATE {} SET {} WHERE {}'.format(self._table_name,
                                                      ', '.join([set + '=?' for set in set_col_names]),
                                                      ' AND '.join([cond + '=?' for cond in cond_col_names]))
        try:
            self._conn.execute(statement, set_params + cond_params)
            return True
        except BaseException as e:
            print("Error @" + str(self._dto_type.__name__) + ":find - " + str(e))
            return False

def orm(cursor, dto_type):
    args = inspect.getfullargspec(dto_type.__init__).args[1:] 
    col_names = [column[0] for column in cursor.description]
    col_mapping = [col_names.index(arg) for arg in args]
    func = lambda _row, _col_mapping, _dto_type: _dto_type(*[_row[idx] for idx in col_mapping])
    return [func(row, col_mapping, dto_type) for row in cursor.fetchall()]