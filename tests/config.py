import pytest
from server import app

@pytest.fixture
def client():
    """ Allows the testing to be launched and under the Testing parameter"""
    client = app.test_client()
    return client

