import unittest
import urllib.request

class DataService(unittest.TestCase):
    def test_connection(self):
        with urllib.request.urlopen("http://127.0.0.1:8080") as response:
            print(response.read())


if __name__ == '__main__':
    unittest.main()
