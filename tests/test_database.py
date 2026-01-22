import pytest
import os
from socials_data.core.db import Database

def test_db_ops():
    db_path = "test_philosophers.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = Database(db_path)
    db.init_db()

    # Test Personality
    db.add_personality("test_p", "Test Philosopher", "Desc", "Prompt")
    p = db.get_personality("test_p")
    assert p["name"] == "Test Philosopher"
    assert p["description"] == "Desc"

    # Test Document
    doc_id = db.add_document("test_p", "test.txt", "Some content")
    assert doc_id is not None

    # Test Chunk
    chunk_id = db.add_chunk(doc_id, "Some content chunk")
    assert chunk_id is not None

    # Test QA
    db.add_qa_pair(chunk_id, "Q?", "A!")

    # Verification queries
    db.connect()
    c = db.conn.cursor()
    c.execute("SELECT count(*) FROM qa_pairs")
    assert c.fetchone()[0] == 1
    db.close()

    os.remove(db_path)
