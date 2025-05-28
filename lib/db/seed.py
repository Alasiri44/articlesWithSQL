from lib.db.connection import get_connection

def seed():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear tables
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    # Insert authors
    cursor.execute("INSERT INTO authors (name) VALUES ('Chinua Achebe')")
    chinua_id = cursor.lastrowid
    cursor.execute("INSERT INTO authors (name) VALUES ('Ngugi wa Thiong\'o')")
    ngugi_id = cursor.lastrowid
    cursor.execute("INSERT INTO authors (name) VALUES ('Margaret Atwood')")
    atwood_id = cursor.lastrowid

    # Insert magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('African Times', 'Culture')")
    african_times_id = cursor.lastrowid
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Global Voice', 'Politics')")
    global_voice_id = cursor.lastrowid
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Literary Digest', 'Literature')")
    digest_id = cursor.lastrowid

    # Insert articles
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('The Roots of Identity', ?, ?)", (chinua_id, african_times_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Colonial Legacy', ?, ?)", (chinua_id, global_voice_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Post-Colonial Lens', ?, ?)", (ngugi_id, african_times_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Eco Fiction', ?, ?)", (atwood_id, digest_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Feminist Voice', ?, ?)", (atwood_id, global_voice_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Dystopian Visions', ?, ?)", (atwood_id, global_voice_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
