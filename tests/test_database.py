import pytest
import tempfile
import os
from datetime import date


@pytest.fixture
def temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    import services.database as db
    monkeypatch.setattr(db, 'DB_FILE', path)
    db.init_db()
    
    yield path
    os.unlink(path)


def test_save_and_get_entry(temp_db):
    from services.database import save_entry, get_entry_by_date
    
    messages = [{"role": "user", "content": "Test"}]
    save_entry("2025-01-01", "Happy", messages)
    
    entry = get_entry_by_date("2025-01-01")
    assert entry is not None
    assert entry['mood'] == "Happy"


def test_get_nonexistent_entry(temp_db):
    from services.database import get_entry_by_date
    
    assert get_entry_by_date("1999-01-01") is None
