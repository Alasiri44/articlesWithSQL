from lib.db.connection import CURSOR, CONN

class Magazine:
    # Dictionary of objects saved to the database
    all = {}
    
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
    
    def __repr__(self):
        return f'<Magazine {self.id}: {self.name}, {self.category}>'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name.strip()) > 0:
            self._name = name
        else:
            raise ValueError(('The name must be a string of length more than zero')) 
            
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category.strip()) > 0:
            self._category = category
        else:
            raise ValueError(('The category must be a string of length more than zero'))   

    @classmethod
    def drop_table(cls):
        """Drop the magazines table that persists the Magazine instances"""
        sql = """
            DROP TABLE IF EXISTS magazines;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Insert a new row with the name and category values of the current Magazine instance
        Update object id using attribute CURSOR.lastrowid
        Save the object in local dictionary using the tables row's PK as dictionary key
        """
        sql = """
            INSERT INTO magazines(name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category ))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, name, category):
        """ Initialize a new magazine instance and save the object to the database """
        magazine = cls(name, category)
        magazine.save()
        return magazine
    
    def update(self):
        """Update the table row corresponding to the current Magazine instance."""
        sql = """
            UPDATE magazines
            SET name = ?, category = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.category, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the table row corresponding to the current Magazine instance,
        delete the dictionary entry, and reassign id attribute"""
        
        sql = """
            DELETE FROM magazines
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
        """Return a magazine object having the attribute values from the table row"""
        magazine = cls.all.get(row[0])
        
        if magazine:
            # ensure attributes match row values in case local instance was modified
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            magazine = cls(row[1], row[2])
            magazine.id = row[0]
            cls.all[magazine.id] = magazine
        return magazine
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Magazine object per table row"""
        sql = """
            SELECT *
            FROM magazines
        """
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]    
        
    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        sql = """
            SELECT *
            FROM magazines
            WHERE id = ?
        """
        
        row = CURSOR.execute(sql, (id, )).fetchone()
        return cls.instance_from_db(row) if row else None
        
    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name"""
        sql = """
            SELECT *
            FROM magazines
            WHERE name = ?
        """
        
        row = CURSOR.execute(sql, (name, )).fetchone()
        return cls.instance_from_db(row) if row else None
        
    @classmethod
    def find_by_category(cls, category):
        """Find a magazine by category"""
        sql = """
            SELECT *
            FROM magazines
            WHERE category = ?
        """
        
        row = CURSOR.execute(sql, (category, )).fetchall()
        return [cls.instance_from_db(row) for row in row] if row else []
        
        
    def contributors(self):
        """Find all authors who have written for a specific magazine"""
        from lib.models.author import Author
        sql = """
            SELECT *
            FROM authors
            INNER JOIN articles AS a
            ON authors.id = a.author_id
            WHERE a.magazine_id = ?
        """
        
        rows = CURSOR.execute(sql, (self.id, )).fetchall()
        return [Author.instance_from_db(row) for row in rows] if rows else []
    
    
    def articles(self):
        """Returns list of all articles published in the magazine (using SQL)"""
        from lib.models.article import Article
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id, )).fetchall()
        return [Article.instance_from_db(row) for row in rows] if rows else []
    
    def article_titles(self):
        """Returns list of titles of all articles published in the magazine (using SQL)"""
        from lib.models.article import Article
        sql = """
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id, )).fetchall()
        return [row[0] for row in rows] if rows else []
    
    def contributing_authors(self):
        """Returns list of authors with more than 2 articles in the magazine"""
        sql = """
            SELECT a.author_id, COUNT(*)
            FROM articles AS a
            WHERE a.magazine_id = ?
            GROUP BY a.author_id
            HAVING COUNT(*) > 2
        """
        rows = CURSOR.execute(sql, (self.id, )).fetchall()
        return [row[0] for row in rows] if rows else []
    
    def total_articles(self):
        """Count the number of articles in each magazine"""
        sql = """
            SELECT COUNT(*)
            FROM articles
            WHERE magazine_id = ?
        """
        row = CURSOR.execute(sql, (self.id, )).fetchone()
        return row[0] if row else 0
        