import pytest
from socials_data.core.db import DBManager
import os

@pytest.fixture
def db():
    # Use in-memory DB for testing
    manager = DBManager(":memory:")
    yield manager
    manager.close()

def test_add_get_personality(db):
    db.add_personality("test_p", "Test Personality")
    p = db.get_personality("test_p")
    assert p["name"] == "Test Personality"
    assert p["id"] == "test_p"

def test_add_get_document_chunk(db):
    db.add_personality("test_p", "Test Personality")
    doc_id = db.add_document("test_p", "test.txt", "content")

    docs = db.get_document_by_filename("test_p", "test.txt")
    assert docs["content"] == "content"

    chunk_id = db.add_chunk(doc_id, "chunk1", 0)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,))
    row = cursor.fetchone()
    assert row[2] == "chunk1"

def test_add_qa_pair(db):
    db.add_personality("test_p", "Test Personality")
    doc_id = db.add_document("test_p", "test.txt", "content")
    chunk_id = db.add_chunk(doc_id, "chunk1", 0)

    db.add_qa_pair(chunk_id, "Q?", "A!", "gpt-3.5", "chunk1")

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM qa_pairs")
    row = cursor.fetchone()
    assert row[2] == "Q?"
    assert row[3] == "A!"
