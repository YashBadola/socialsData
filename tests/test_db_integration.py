import pytest
import shutil
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import Database

@pytest.fixture
def temp_personality_id():
    pid = "test_philosopher"
    manager = PersonalityManager()
    # Cleanup if exists
    target_dir = manager.base_dir / pid
    if target_dir.exists():
        shutil.rmtree(target_dir)

    manager.create_personality("Test Philosopher")
    yield pid

    # Teardown
    if target_dir.exists():
        shutil.rmtree(target_dir)

    # Also remove from DB?
    # The current DB implementation doesn't have a delete method, but that's fine for now.

def test_db_integration(temp_personality_id):
    manager = PersonalityManager()
    db = Database()

    # Verify personality in DB
    p = db.get_personality(temp_personality_id)
    assert p is not None
    assert p['name'] == "Test Philosopher"

    # Create a raw file
    raw_dir = manager.base_dir / temp_personality_id / "raw"
    test_file = raw_dir / "test.txt"
    content = "This is a test document content."
    with open(test_file, "w") as f:
        f.write(content)

    # Process
    processor = TextDataProcessor()
    processor.process(manager.base_dir / temp_personality_id, skip_qa=True)

    # Verify document in DB
    db.connect()
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE personality_id = ?", (temp_personality_id,))
    doc = cursor.fetchone()
    assert doc is not None
    assert doc['filename'] == "test.txt"
    # Note: TextDataProcessor cleans text, so it might be slightly different if cleaning does anything.
    # The current cleaning just strips lines.
    assert doc['content'] == content

    # Verify chunk in DB
    cursor.execute("SELECT * FROM chunks WHERE document_id = ?", (doc['id'],))
    chunk = cursor.fetchone()
    assert chunk is not None
    assert chunk['text'] == content

    db.close()
