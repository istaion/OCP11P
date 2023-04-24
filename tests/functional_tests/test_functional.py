import time
from selenium import webdriver
from tests.config import client, mock_data
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
import os

install_dir = "/snap/firefox/current/usr/lib/firefox"
driver_loc = os.path.join(install_dir, "geckodriver")
binary_loc = os.path.join(install_dir, "firefox")

service = FirefoxService(driver_loc)
opts = webdriver.FirefoxOptions()
opts.binary_location = binary_loc
driver = webdriver.Firefox(service=service, options=opts)

url_root = 'http://127.0.0.1:5000/'


@pytest.mark.usefixtures('client', 'mock_data')
class TestsFunctional:
    def test_functional_login(self):
        driver.get(url_root)
        email_form = driver.find_element(By.ID, 'email')
        time.sleep(1)
        email_form.clear()
        time.sleep(1)
        email_form.send_keys('john@simplylift.co')
        time.sleep(1)
        button_login = driver.find_element(By.TAG_NAME, 'button')
        time.sleep(1)
        button_login.click()
        time.sleep(1)
        assert driver.find_element(By.TAG_NAME, 'h2').text == 'Welcome, john@simplylift.co'

    def test_functional_purchase(self, client):
        comp = driver.find_element(By.ID, 'Spring Festival').find_element(By.TAG_NAME, 'a')
        time.sleep(1)
        comp.click()
        time.sleep(1)
        form = driver.find_element(By.ID, 'places')
        form.clear()
        form.send_keys(3)
        time.sleep(1)
        button_book = driver.find_element(By.TAG_NAME, 'button')
        button_book.click()
        time.sleep(1)
        assert 'Great-booking complete!' == driver.find_element(By.ID, 'messages').text

    def test_functional_logout(self):
        driver.close()
