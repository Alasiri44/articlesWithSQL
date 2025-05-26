from connection import get_connection

def seed_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.executescript("""
    DELETE FROM articles;
    DELETE FROM magazines;
    DELETE FROM authors;
    """)

    # Insert Authors
    cursor.executemany("""
    INSERT INTO authors (name) VALUES (?);
    """, [
        ("Chinua Achebe",),
        ("Margaret Atwood",),
        ("George Orwell",),
        ("Zadie Smith",),
        ("Toni Morrison",),
    ])

    # Insert Magazines
    cursor.executemany("""
    INSERT INTO magazines (name, category) VALUES (?, ?);
    """, [
        ("The Atlantic", "Politics"),
        ("National Geographic", "Science"),
        ("New Yorker", "Literature"),
        ("Wired", "Technology"),
        ("Time", "News"),
    ])

    # Insert Articles
    cursor.executemany("""
    INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?);
    """, [
        ("The Future of AI", 3, 4),
        ("Under the Baobab", 1, 3),
        ("Digital Freedom", 3, 1),
        ("Literary Queens", 2, 3),
        ("Race and Reality", 5, 5),
        ("Feminism in the North", 2, 5),
        ("Beyond Borders", 4, 2),
        ("Nature Speaks", 4, 2),
        ("Data and Dignity", 3, 4),
        ("Voices of Africa", 1, 1),
        ("Through the Lens", 5, 2),
        ("Power and People", 5, 1),
        ("Poetry in Crisis", 2, 3),
        ("Youth in Tech", 4, 4),
        ("Migrations", 1, 2),
    ])

    conn.commit()
    conn.close()
    print("🌱 Seeded the database with dummy data.")
    
seed_db()