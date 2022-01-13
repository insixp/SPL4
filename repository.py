import sqlite3

class REPOSITORY:
    def __init__(self, db_name):
        self._db = sqlite3.connect(db_name)
    
    def create_table(self):
        try:
            self._db.executescript("""
            CREATE TABLE suppliers(
                id INTEGER PRIMARY KEY,
                name STRING NOT NULL
            );

            CREATE TABLE hats(
                id INTEGER PRIMARY KEY,
                topping STRING NOT NULL,
                supplier INTEGER REFERENCES suppliers(id),
                quantity INTEGER NOT NULL
            );

            CREATE TABLE orders(
                id INTEGER PRIMARY KEY,
                location STRING NOT NULL,
                hat INTEGER REFERENCES hats(id)
            );
            """)
            self._db.commit()
        except BaseException as e:
            self.dropTables()
            self.create_table()
    
    def dropTables(self):
        self._db.executescript("""
                DROP TABLE suppliers;
                DROP TABLE hats;
                DROP TABLE orders;
            """)

    def getConnection(self):
        return self._db

    def commit(self):
        self._db.commit()