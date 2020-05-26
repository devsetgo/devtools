# -*- coding: utf-8 -*-
import unittest
import uuid

# from starlette.testclient import TestClient
from async_asgi_testclient import TestClient as Async_TestClient
from main import app

client = Async_TestClient(app)


class Test(unittest.TestCase):
    async def test_home(self):

        url = f"/pypi"
        response = await client.get(url)
        assert response.status_code == 200
        # assert "X-Process-Time" in response.headers

    # async def test_index(self):

    #     url = f"/index"
    #     response = await client.get(url)
    #     # assert response.status_code == 200
    #     assert response.status_code == 200
    #     # assert "X-Process-Time" in response.headers

    # async def test_index__error(self):
    #     uid = uuid.uuid1()
    #     url = f"/{uid}"
    #     response = await client.get(url)
    #     assert response.status_code == 404
