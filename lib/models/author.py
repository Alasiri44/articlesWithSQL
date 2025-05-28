from lib.db.connection import CURSOR, CONN

class Author:
    #Dictionary of objects saved to the database
    all = {}
    
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str) or len(name.strip()) < 1:
            raise ValueError('The name must be a string of length more than zero')
        else:
            self._name = name
        
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the Author instances"""
        sql = """
            DROP TABLE IF EXISTS authors;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Insert a new ro with the name value of the current Author instance
        Update id attribute with the last inserted row id
        Save the object in local dictionary using the tables row's PK as dictionary key
        """
        sql = """
            INSERT INTO authors(name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name, ))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    def update(self):
        """Update the table row corresponding to the current Author instance."""
        sql = """
            UPDATE authors
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the table row corresponding to the current Author instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM authors
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
    
    @classmethod
    def create(cls, name, job_title, department_id):
        """ Initialize a new Author instance and save the object to the database """
        author = cls(name)
        author.save()
        return author
    
    @classmethod
    def instance_from_db(cls, row):
        """Create an Author instance from a database row"""
        author = cls.all.get(row[0])
        if author:
            # ensure attributes match row values in case local instance was modified
            author.name = row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            author = cls(row[1])
            author.id = row[0]
            cls.all[row[0]] = author
        return author
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Author object per table row"""
        sql = """
            SELECT *
            FROM authors
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID"""
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """
        row =  CURSOR.execute(sql, (id, )).fetchone()
        return cls.instance_from_db(row) if row else None
        
    @classmethod
    def find_by_name(cls, name):
        """Find an author by name"""
        sql = """
            SELECT *
            FROM authors
            WHERE name = ?
        """
        row =  CURSOR.execute(sql, (name, )).fetchone()
        return cls.instance_from_db(row) if row else None
        
    def articles(self):
        """Get all articles written by a specific author"""
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """

        return [article for article in CURSOR.execute(sql, (self.id,) ).fetchall()]
    
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
    

