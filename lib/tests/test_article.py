import pytest
from lib.models.article import Article
from lib.db.connection import CURSOR, CONN

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: create a clean articles table before each test
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL
        )
    """)
    CONN.commit()
    
    # Clear the table content and Article.all dictionary before each test
    CURSOR.execute("DELETE FROM articles")
    CONN.commit()
    Article.all.clear()
    
    yield
    
    # Teardown: drop the table after each test
    Article.drop_table()
    Article.all.clear()


def test_create_and_save_article():
    article = Article.create("Test Title", 1, 2)
    assert article.id is not None
    assert article.title == "Test Title"
    assert article.author_id == 1
    assert article.magazine_id == 2
    assert article.id in Article.all
    # Confirm in DB
    CURSOR.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    row = CURSOR.fetchone()
    assert row[1] == "Test Title"


def test_update_article():
    article = Article.create("Original Title", 1, 2)
    article.title = "Updated Title"
    article.update()
    # Check DB row updated
    CURSOR.execute("SELECT title FROM articles WHERE id = ?", (article.id,))
    row = CURSOR.fetchone()
    assert row[0] == "Updated Title"


def test_delete_article():
    article = Article.create("To be deleted", 1, 2)
    id_ = article.id
    article.delete()
    assert article.id is None
    assert id_ not in Article.all
    # Confirm deleted from DB
    CURSOR.execute("SELECT * FROM articles WHERE id = ?", (id_,))
    assert CURSOR.fetchone() is None


def test_find_by_id():
    article = Article.create("Find me", 3, 4)
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.id == article.id
    assert found.title == "Find me"


def test_find_by_author_id():
    article = Article.create("Author Article", 99, 5)
    found = Article.find_by_author_id(99)
    assert found is not None
    assert found.author_id == 99


def test_find_by_magazine_id():
    article = Article.create("Magazine Article", 6, 77)
    found = Article.find_by_magazine_id(77)
    assert found is not None
    assert found.magazine_id == 77


def test_get_all_returns_all_articles():
    a1 = Article.create("Title 1", 1, 1)
    a2 = Article.create("Title 2", 2, 2)
    all_articles = Article.get_all()
    ids = [article.id for article in all_articles]
    assert a1.id in ids
    assert a2.id in ids