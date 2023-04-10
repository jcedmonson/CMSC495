import unittest
import urllib.error
from urllib import request
from urllib.parse import urlencode


def _get_data(**kwargs) -> bytes:
    """Quick helper function to convert a dict into a byte array"""
    return urlencode(kwargs).encode("UTF-8")


class DataService(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1:8080"

    def get_request(self, uri: str, **kwargs):
        req = request.Request(f"{self.base_url}/{uri}",
                              data=_get_data(**kwargs),
                              headers={"Content-Type": "application/json"})

        return req

    def test_connection(self):
        with request.urlopen(self.base_url) as response:
            self.assertIsNotNone(response)

    def test_invalid_login(self):
        req = self.get_request("login", email="Email", password="password")
        print(req.data)

        try:
            with request.urlopen(req) as response:
                print(response.read())
        except urllib.error.HTTPError as error:
            self.fail(msg=f"{error.status}: {error.reason}\n{error.read().decode()}")
        except urllib.error.URLError as error:
            self.fail(error.reason)

    if __name__ == '__main__':
        unittest.main()
