from db.connection import CURSOR, CONN

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f'<Author {self.id} {self.name}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            ValueError(('The name must be a string of length more than zero'))
    
    @classmethod
    def create_table(cls):
        """Create an authors table with columns"""
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the authors table"""
        sql = """
            DROP TABLE authors IF EXISTS;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Save an author to the database"""
        sql = """
            INSERT INTO authors(name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name, ))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID"""
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """
        CURSOR.execute(sql, (id, ))
        CONN.commit()
        
    @classmethod
    def find_by_name(cls, name):
        """Find an author by name"""
        sql = """
            SELECT *
            FROM authors
            WHERE name = ?
        """
        CURSOR.execute(sql, (name, ))
        CONN.commit()
        
    def articles(self):
        