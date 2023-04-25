import time
from selenium import webdriver
import tests.config as config
from selenium.webdriver.common.by import By
from flask_testing import LiveServerTestCase


class TestsFunctional(LiveServerTestCase):
    def create_app(self):
        app = config.selenium_create_app()
        return app

    def setUp(self):
        self.driver = webdriver.Firefox(service=config.service, options=config.opts)

    def tearDown(self):
        self.driver.quit()

    def test_functional(self):
        # login
        self.driver.get(config.url_root)
        email_form = self.driver.find_element(By.ID, 'email')
        email_form.clear()
        time.sleep(1)
        email_form.send_keys('john@simplylift.co')
        time.sleep(1)
        button_login = self.driver.find_element(By.TAG_NAME, 'button')
        button_login.click()
        time.sleep(1)
        assert self.driver.find_element(By.TAG_NAME, 'h2').text == 'Welcome, john@simplylift.co'
        # purchase
        comp = self.driver.find_element(By.ID, 'Spring Festival').find_element(By.TAG_NAME, 'a')
        comp.click()
        time.sleep(1)
        form = self.driver.find_element(By.ID, 'places')
        form.clear()
        form.send_keys(3)
        time.sleep(1)
        button_book = self.driver.find_element(By.TAG_NAME, 'button')
        button_book.click()
        time.sleep(1)
        assert 'Great-booking complete!' == self.driver.find_element(By.ID, 'messages').text
        # check point
        button_points = self.driver.find_element(By.ID, 'show_points')
        button_points.click()
        time.sleep(1)
        points = self.driver.find_element(By.ID, 'Simply Lift').text
        assert points == 'Simply Lift 10'
        time.sleep(1)
        # logout
        self.driver.back()
        time.sleep(1)
        button_logout = self.driver.find_element(By.ID, 'logout')
        button_logout.click()
        time.sleep(1)
        assert 'Welcome to the GUDLFT Registration Portal!' == self.driver.find_element(By.TAG_NAME, 'h1').text
