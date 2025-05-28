import pytest
from lib.models.author import Author
from lib.db.connection import CURSOR, CONN

@pytest.fixture(autouse=True, scope="module")
def setup_module():
    # Recreate the authors table before the tests
    CURSOR.execute("DROP TABLE IF EXISTS authors")
    CURSOR.execute("""
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)
    CONN.commit()
    yield
    CURSOR.execute("DELETE FROM authors")
    CONN.commit()
    Author.all = {}

@pytest.fixture(autouse=True)
def clear_authors_table():
    # Clear authors before each test
    CURSOR.execute("DELETE FROM authors")
    CONN.commit()
    Author.all.clear()

def test_create_and_save_author():
    author = Author("John Doe")
    author.save()

    assert author.id is not None
    assert author.id in Author.all
    assert Author.all[author.id] == author

def test_name_validation():
    with pytest.raises(ValueError):
        Author("").save()

def test_update_author():
    author = Author("Jane Doe")
    author.save()
    author.name = "Jane Smith"
    author.update()

    updated = Author.find_by_id(author.id)
    assert updated.name == "Jane Smith"

def test_delete_author():
    author = Author("Mark Twain")
    author.save()
    author_id = author.id
    author.delete()

    assert author.id is None
    assert author_id not in Author.all
    assert Author.find_by_id(author_id) is None

def test_find_by_id():
    author = Author("Albert Einstein")
    author.save()
    found = Author.find_by_id(author.id)

    assert found.name == "Albert Einstein"

def test_find_by_name():
    author = Author("Isaac Newton")
    author.save()
    found = Author.find_by_name("Isaac Newton")

    assert found.id == author.id

def test_get_all():
    a1 = Author("Author A")
    a1.save()
    a2 = Author("Author B")
    a2.save()

    authors = Author.get_all()
    assert len(authors) == 2
    assert any(a.name == "Author A" for a in authors)
    assert any(a.name == "Author B" for a in authors)
