import inspect

def orm(cursor, dto_type):
    args = inspect.getfullargspec(dto_type.__init__).args[1:0] 
    col_names = [column[0] for column in cursor.description]
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]