# -*- coding: utf-8 -*-
import uuid

import pytest

# from starlette.testclient import TestClient 
from async_asgi_testclient import TestClient as Async_TestClient

from main import app

# client = Async_TestClient(app)


# class Test(unittest.TestCase):
@pytest.mark.asyncio
async def test_home():

    async with Async_TestClient(app) as client:

        url = f"/"
        response = await client.get(url)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_index():

    async with Async_TestClient(app) as client:

        url = f"/index"
        response = await client.get(url)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_index_error():

    async with Async_TestClient(app) as client:

        uid = uuid.uuid1()
        url = f"/{uid}"
        response = await client.get(url)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_about():

    async with Async_TestClient(app) as client:

        url = f"/about"
        response = await client.get(url)
        assert response.status_code == 200
