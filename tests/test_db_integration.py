import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import Database
import shutil

def test_db_flow():
    # Setup
    manager = PersonalityManager()
    p_id = "test_philosopher"

    # Clean up previous run if any
    try:
        shutil.rmtree(manager.base_dir / p_id)
    except FileNotFoundError:
        pass

    # 1. Create Personality
    manager.create_personality("Test Philosopher")

    # Verify in DB
    db = Database()
    p = db.get_personality(p_id)
    assert p is not None
    assert p['name'] == "Test Philosopher"

    # 2. Add Raw Data
    raw_dir = manager.base_dir / p_id / "raw"
    with open(raw_dir / "test_doc.txt", "w") as f:
        f.write("This is a test document.\nIt has multiple lines.")

    # 3. Process
    processor = TextDataProcessor()
    processor.process(manager.base_dir / p_id, skip_qa=True)

    # 4. Verify DB Data
    db.connect()
    cursor = db.conn.cursor()

    # Check Document
    cursor.execute("SELECT * FROM documents WHERE personality_id=?", (p_id,))
    doc = cursor.fetchone()
    assert doc is not None
    assert doc['filename'] == "test_doc.txt"

    # Check Chunk
    cursor.execute("SELECT * FROM chunks WHERE document_id=?", (doc['id'],))
    chunk = cursor.fetchone()
    assert chunk is not None
    assert "This is a test document." in chunk['text']

    db.close()

    # Cleanup
    shutil.rmtree(manager.base_dir / p_id)
    # Also clean DB? ideally yes but for now we just check functionality.

if __name__ == "__main__":
    test_db_flow()
