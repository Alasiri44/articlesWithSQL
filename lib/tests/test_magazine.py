import pytest
from lib.models.magazine import Magazine
from lib.db.connection import CURSOR, CONN

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    # Drop and create magazines table before all tests
    CURSOR.execute("DROP TABLE IF EXISTS magazines")
    CURSOR.execute("""
        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT
        )
    """)
    CONN.commit()
    yield
    CURSOR.execute("DELETE FROM magazines")
    CONN.commit()
    Magazine.all = {}

@pytest.fixture(autouse=True)
def clear_magazines_table():
    # Clear table and dict before each test
    CURSOR.execute("DELETE FROM magazines")
    CONN.commit()
    Magazine.all.clear()

def test_create_and_save_magazine():
    mag = Magazine("Tech Today", "Technology")
    mag.save()

    assert mag.id is not None
    assert mag.id in Magazine.all
    assert Magazine.all[mag.id] == mag

def test_name_validation():
    with pytest.raises(ValueError):
        mag = Magazine("", "Tech")
        mag.save()

def test_category_validation():
    with pytest.raises(ValueError):
        mag = Magazine("Tech Today", "")
        mag.save()

def test_update_magazine():
    mag = Magazine("Health Monthly", "Health")
    mag.save()
    mag.name = "Health Weekly"
    mag.category = "Wellness"
    mag.update()

    updated = Magazine.find_by_id(mag.id)
    assert updated.name == "Health Weekly"
    assert updated.category == "Wellness"

def test_delete_magazine():
    mag = Magazine("Sports Weekly", "Sports")
    mag.save()
    mag_id = mag.id
    mag.delete()

    assert mag.id is None
    assert mag_id not in Magazine.all
    assert Magazine.find_by_id(mag_id) is None

def test_find_by_id_and_name():
    mag = Magazine("Nature Daily", "Environment")
    mag.save()

    found_by_id = Magazine.find_by_id(mag.id)
    found_by_name = Magazine.find_by_name("Nature Daily")

    assert found_by_id.id == mag.id
    assert found_by_name.id == mag.id

def test_find_by_category():
    m1 = Magazine("Auto World", "Cars")
    m2 = Magazine("Speed", "Cars")
    m1.save()
    m2.save()

    cars_mags = Magazine.find_by_category("Cars")
    assert len(cars_mags) == 2
    assert all(isinstance(m, Magazine) for m in cars_mags)

def test_get_all():
    mag1 = Magazine("Cooking Times", "Food")
    mag2 = Magazine("Travel Explorer", "Travel")
    mag1.save()
    mag2.save()

    all_mags = Magazine.get_all()
    assert len(all_mags) == 2
    names = [m.name for m in all_mags]
    assert "Cooking Times" in names
    assert "Travel Explorer" in names
