def create_table():
        """Create an authors table with columns"""
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
        