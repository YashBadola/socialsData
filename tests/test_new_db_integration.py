import unittest
from socials_data.core.db import Database
from socials_data.core.manager import PersonalityManager
from pathlib import Path

class TestNewDBIntegration(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        # Ensure we connect to the main DB
        self.db.init_db()

    def test_kierkegaard_in_db(self):
        p = self.db.get_personality("søren_kierkegaard")
        self.assertIsNotNone(p)
        self.assertEqual(p['name'], "Søren Kierkegaard")

    def test_documents_in_db(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE personality_id = 'søren_kierkegaard'")
        docs = cursor.fetchall()
        self.assertTrue(len(docs) > 0)

        doc_id = docs[0]['id']
        cursor.execute("SELECT * FROM chunks WHERE document_id = ?", (doc_id,))
        chunks = cursor.fetchall()
        self.assertTrue(len(chunks) > 0)
        self.db.close()

if __name__ == '__main__':
    unittest.main()
