import os
import visilist
import unittest


class VisilistTestCase(unittest.TestCase):

    def setUp(self):
        self.app = visilist.app.test_client()

    def tearDown(self):
        pass

    def login(self, email, pass):
        dat = dict(email=email, password=pass)
        return self.app.post('/login', data=dat)

    def new_list(self, name, type, url):
        li = List()
        li.name = name
        li.type = type
        li.list_url = url
        return self.app.post(li.__dict__)

    def test_login(self):
        self.login('alto50@gmail.com', 'testing')
        assert 'WHOA!'

    def test_newlist(self):
        dat

if __name__ == '__main__':
    unittest.main()
