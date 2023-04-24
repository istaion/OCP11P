from tests.config import client, mock_data
import pytest


@pytest.mark.usefixtures('client', 'mock_data')
class TestsUnitLogin:
    def test_index(self, client):
        response = client.get('/')
        response_data = response.data.decode()
        assert response.status_code == 200
        assert '<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response_data

    def test_rankings(self, client):
        response = client.get('/show_points')
        response_data = response.data.decode()
        assert response.status_code == 200
        assert '<td>Club :</td>' in response_data
        assert '<td>Points :</td>' in response_data

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == 302

    def test_login(self, client):
        response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        assert 'Welcome' in response.data.decode()
        assert 'john@simplylift.co ' in response.data.decode()

    def test_login_wrong_mail(self, client):
        email = 'test.fail@email.com'
        response = client.post('/show_summary', data={'email': email})
        assert response.status_code == 200
        assert 'Sorry, that email was not found' in response.data.decode()
