# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from main import app

client = TestClient(app)


class Test(unittest.TestCase):
    def test_health_pages(self):

        url = f"/health"
        client = TestClient(app)
        response = client.get(url)
        assert response.status_code == 200
