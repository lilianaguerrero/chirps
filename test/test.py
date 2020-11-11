"""Unittests for Bellbird Project"""

from server import app
import unittest

class MyTest(unittest.TestCase):
    def test_index(self):
        client = app.test_client()
        result = client.get('/index')
        self.assertEqual(result.status_code, 200)

if __name__ == "__main__":
    unittest.main()