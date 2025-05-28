from lib.db.connection import CURSOR, CONN

class Article:
    # Dictionary of objects saved to the database.
    all = {}
    
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    def __repr__(self):
        return f'<article {self.id}: {self.title}, {self.author_id} ,{self.magazine_id}>'

    @classmethod
    def drop_table(cls):
        """Drop the articles table that persists the Article instances"""
        sql = """
            DROP TABLE IF EXISTS articles;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Insert a new row with the title, author_id, and magazine_id values of the current Article instance"""
        sql = """
            INSERT INTO articles(title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id ))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, title, author_id, magazine_id):
        """Initialize a new Article instance and save it to the database"""
        article = cls(title, author_id, magazine_id)
        article.save()
        return article
    
    def update(self):
        """Update the table row corresponding to the current Article instance."""
        sql = """
            UPDATE articles
            SET title = ?, author_id = ?, magazine_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the table row corresponding to the current Article instance,
        delete the dictionary entry, and reassign id attribute"""
        
        sql = """
            DELETE FROM articles
            WHERE id = ?
        """
        
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]
        
        # Set the id to None
        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        """Return an article object having the attribute values from the database row"""
        
        # Check the dictionary for an existing instance from the rows primary key
        article = cls.all.get(row[0])
        
        if article:
            article.title = row[1]
            article.author_id = row[2]
            article.magazine_id = row[3]
        else:
            # Not in dictionary, create new instance and add to dictionary
            article = cls(row[1], row[2], row[3])
            article.id = row[0]
            cls.all[article.id] = article
        return article
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Article object per table row"""
        sql = """
            SELECT *
            FROM articles
        """
        CURSOR.execute(sql)
        CONN.commit()
        
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
        
    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        sql = """
            SELECT *
            FROM articles
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id, )).fetchone()
        return cls.instance_from_db(row) if row else None
       
    @classmethod
    def find_by_author_id(cls, author_id):
        """Find an article by author_id"""
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        row = CURSOR.execute(sql, (author_id, )).fetchone()
        return cls.instance_from_db(row) if row else None
        
    @classmethod
    def find_by_magazine_id(cls, magazine_id):
        """Find an article by magazine_id"""
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        row = CURSOR.execute(sql, (magazine_id, )).fetchone()
        return cls.instance_from_db(row) if row else None