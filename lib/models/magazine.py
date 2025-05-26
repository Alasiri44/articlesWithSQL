from db.connection import CURSOR, CONN

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
    
    def __repr__(self):
        return f'<Magazine {self.id} {self.name} {self.category}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            ValueError(('The name must be a string of length more than zero')) 
            
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            ValueError(('The category must be a string of length more than zero'))   
    
    @classmethod
    def create_table(cls):
        """Create an magazines table with columns"""
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
            category VARCHAR(255) NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """Drop the magazines table"""
        sql = """
            DROP TABLE magazines IF EXISTS;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Save an magazine to the database"""
        sql = """
            INSERT INTO magazines(name, category)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name, self.category ))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        sql = """
            SELECT *
            FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql, (id, ))
        CONN.commit()
        
    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name"""
        sql = """
            SELECT *
            FROM magazines
            WHERE name = ?
        """
        CURSOR.execute(sql, (name, ))
        CONN.commit()
        
    @classmethod
    def find_by_category(cls, category):
        """Find a magazine by category"""
        sql = """
            SELECT *
            FROM magazines
            WHERE category = ?
        """
        CURSOR.execute(sql, (category, ))
        CONN.commit()
        
    def contributors(self):
        """Find all authors who have written for a specific magazine"""
        sql = """
            SELECT *
            FROM authors
            INNER JOIN articles AS a
            ON authors.id = a.author_id
            WHERE a.magazine_id = ?
        """
        return [author.name for author in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def articles(self):
        """Returns list of all articles published in the magazine (using SQL)"""
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        return [article for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def article_titles(self):
        """Returns list of titles of all articles published in the magazine (using SQL)"""
        sql = """
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """
        return [article for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def contributing_authors(self):
        """Returns list of authors with more than 2 articles in the magazine"""
        sql = """
            SELECT authors.name, COUNT(articles.id)
            FROM authors, articles
            INNER JOIN articles AS a
            ON authors.id = a.author_id
            WHERE a.magazine_id = ? 
            GROUP BY name 
            WHERE COUNT(articles.id) > 2
        """
        return [author.name for author in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
    def total_articles(self):
        """Count the number of articles in each magazine"""
        sql = """
            SELECT COUNT(id)
            FROM articles
            WHERE magazine_id = ?
        """
        
    
    