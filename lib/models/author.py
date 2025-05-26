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
        """Get all articles written by a specific author"""
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        return [article.title for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def magazines(self):
        """Find all magazines a specific author has contributed to"""
        sql = """
            SELECT *
            FROM magazines AS m
            INNER JOIN articles AS a 
            ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """
        return [article.name for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def add_article(self, magazine, title):
        from article import Article
        Article(title, self.id, magazine.id)
        
    def topic_areas(self):
        """Returns unique list of categories of magazines the author has contributed to"""
        sql = """
            SELECT category
            FROM magazines AS m
            INNER JOIN articles AS a 
            ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """
        return [article.name for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def most_contributing_author(self):
        """Find the author who has written the most articles"""
        pass