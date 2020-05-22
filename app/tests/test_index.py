# -*- coding: utf-8 -*-
import unittest
import uuid
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from main import app

# client = TestClient(app)


class Test(unittest.TestCase):
    def test_index(self):

        # url = f"/twitter-bots"
        # client = TestClient(app)
        # response = client.get(url)
        # assert response.status_code == 200
        with TestClient(app) as client:

            url = f"/twitter-bots"
            result = client.get(url)
            # self.assertEqual(result.status_code, 303)
            assert result.status_code == 200

        # assert response.status_code == 200

    # def test_index__error(self):
    #     uid = uuid.uuid1()
    #     url = f"/index/{uid}"
    #     response = client.get(url)
    #     assert response.status_code == 404

    def test_health_pages(self):

        url = f"/health"
        client = TestClient(app)
        response = client.get(url)
        assert response.status_code == 200
