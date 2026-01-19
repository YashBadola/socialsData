from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import Database
import pytest
import os

def test_kierkegaard_end_to_end():
    # 1. Setup: Ensure DB is operational
    # Manager init calls init_db and sync_db
    manager = PersonalityManager()

    # 2. Run processing
    processor = TextDataProcessor()

    personality_id = "søren_kierkegaard"
    personality_dir = manager.base_dir / personality_id

    assert personality_dir.exists(), "Personality directory must exist for test"

    # Run process (this populates the DB)
    processor.process(personality_dir, skip_qa=True)

    # 3. Verify DB content
    db = Database()
    with db:
        cursor = db.conn.cursor()

        # Check Personality
        cursor.execute("SELECT * FROM personalities WHERE id=?", (personality_id,))
        p = cursor.fetchone()
        assert p is not None
        assert p["name"] == "Søren Kierkegaard"

        # Check Document
        cursor.execute("SELECT * FROM documents WHERE personality_id=?", (personality_id,))
        doc = cursor.fetchone()
        assert doc is not None
        assert "fear_and_trembling" in doc["filename"]

        # Check Chunk
        cursor.execute("SELECT * FROM chunks WHERE document_id=?", (doc["id"],))
        chunk = cursor.fetchone()
        assert chunk is not None
        assert "Faith is precisely this paradox" in chunk["text"]

        # Verify idempotency (run again)
    processor.process(personality_dir, skip_qa=True)

    with db:
        cursor = db.conn.cursor()
        # Should still have same number of documents (1) not 2
        cursor.execute("SELECT COUNT(*) FROM documents WHERE personality_id=?", (personality_id,))
        count = cursor.fetchone()[0]
        assert count == 1, "Process should be idempotent"

if __name__ == "__main__":
    test_kierkegaard_end_to_end()
