# -*- coding: utf-8 -*-
import unittest

# from starlette.testclient import TestClient
from async_asgi_testclient import TestClient
from main import app

client = TestClient(app)


class Test(unittest.TestCase):
    async def test_home(self):

        url = f"/"
        response = await client.get(url)
        assert response.status_code == 303
        # assert "X-Process-Time" in response.headers

    async def test_index(self):

        url = f"/index"
        response = await client.get(url)
        # assert response.status_code == 200
        assert response.status_code == 200
        # assert "X-Process-Time" in response.headers

    # def test_index__error(self):
    #     uid = uuid.uuid1()
    #     url = f"/index/{uid}"
    #     response = client.get(url)
    #     assert response.status_code == 404
