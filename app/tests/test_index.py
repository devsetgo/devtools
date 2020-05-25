# -*- coding: utf-8 -*-
import unittest
import uuid
from starlette.testclient import TestClient
from main import app

client = TestClient(app)


class Test(unittest.TestCase):
    def test_index(self):

        url = f"/index"
        response = client.get(url)
        assert response.status_code == 200

    # def test_index__error(self):
    #     uid = uuid.uuid1()
    #     url = f"/index/{uid}"
    #     response = client.get(url)
    #     assert response.status_code == 404
