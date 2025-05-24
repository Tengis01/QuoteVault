import unittest
import json
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        
        self.db_path = "test_quotes.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                quote TEXT NOT NULL
            )
        """)
        self.conn.commit()
       
        os.environ["MYSQL_HOST"] = "sqlite"
        os.environ["MYSQL_DATABASE"] = self.db_path

    def tearDown(self):
        
        self.cursor.close()
        self.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_quotes(self):
     
        response = self.client.get('/quotes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

        self.cursor.execute("INSERT INTO quotes (author, quote) VALUES (?, ?)", 
                          ("Test Author", "Test Quote"))
        self.conn.commit()
        response = self.client.get('/quotes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['author'], "Test Author")
        self.assertEqual(data[0]['quote'], "Test Quote")

    def test_add_quote(self):
        
        response = self.client.post('/quotes', 
                                  data=json.dumps({
                                      "author": "Confucius",
                                      "quote": "Life is really simple, but we insist on making it complicated."
                                  }), 
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Quote added")

       
        self.cursor.execute("SELECT * FROM quotes WHERE author = ?", ("Confucius",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Confucius")
        self.assertEqual(result[2], "Life is really simple, but we insist on making it complicated.")

    def test_add_quote_invalid_data(self):
        
        response = self.client.post('/quotes',
                                  data=json.dumps({
                                      "quote": "Missing author"
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/quotes',
                                  data=json.dumps({
                                      "author": "No quote"
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_random_quote(self):
      
        response = self.client.get('/quotes/random')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "No quotes found")

       
        self.cursor.execute("INSERT INTO quotes (author, quote) VALUES (?, ?)",
                          ("Test Author", "Test Quote"))
        self.conn.commit()
        response = self.client.get('/quotes/random')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('author', data)
        self.assertIn('quote', data)
        self.assertEqual(data['author'], "Test Author")
        self.assertEqual(data['quote'], "Test Quote")

if __name__ == '__main__':
    unittest.main()