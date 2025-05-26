from db.connection import CURSOR, CONN

class Article:
    all = {}
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    def __repr__(self):
        return f'<article {self.id} {self.name} {self.category}>'
    
    @classmethod
    def create_table(cls):
        """Create an articles table with columns"""
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES articles(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """Drop the articles table"""
        sql = """
            DROP TABLE articles IF EXISTS;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Save an article to the database"""
        sql = """
            INSERT INTO articles(title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id ))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        sql = """
            SELECT *
            FROM articles
            WHERE id = ?
        """
        CURSOR.execute(sql, (id, ))
        CONN.commit()
        
    @classmethod
    def find_by_author_id(cls, author_id):
        """Find an article by author_id"""
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        CURSOR.execute(sql, (author_id, ))
        CONN.commit()
        
    @classmethod
    def find_by_magazine_id(cls, magazine_id):
        """Find an article by magazine_id"""
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (magazine_id, ))
        CONN.commit()