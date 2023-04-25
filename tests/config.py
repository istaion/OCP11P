import pytest
import server
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import os


@pytest.fixture
def client():
    """ Allows the testing to be launched and under the Testing parameter"""
    client = server.app.test_client()
    return client


def mock_competitions():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "test place",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "10"
        }
    ]
    return competitions


def mock_clubs():
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "500"
        }
    ]
    return clubs


@pytest.fixture
def mock_data(mocker):
    mocker.patch.object(server, 'competitions', mock_competitions())
    mocker.patch.object(server, 'clubs', mock_clubs())
    return mocker


# configuration for selenium : install_dir : path to firefox

install_dir = "/snap/firefox/current/usr/lib/firefox"
driver_loc = os.path.join(install_dir, "geckodriver")
binary_loc = os.path.join(install_dir, "firefox")

service = FirefoxService(driver_loc)
opts = webdriver.FirefoxOptions()
opts.binary_location = binary_loc

url_root = 'http://127.0.0.1:5000/'


def selenium_create_app():
    app = server.app
    app.config['TESTING'] = True
    server.competitions = mock_competitions()
    server.clubs = mock_clubs()
    return app
