from tests.config import client
import pytest


@pytest.mark.usefixtures("client")
class Tests:
    def test_index(self, client):
        response = client.get('/')
        response_data = response.data.decode()
        assert response.status_code == 200
        assert '<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response_data

    def test_rankings(self, client):
        response = client.get('/showPoints')
        response_data = response.data.decode()
        assert response.status_code == 200
        assert '<td>Club :</td>' in response_data
        assert '<td>Points :</td>' in response_data

    def test_logout(self, client):
        response = client.get('/logout')
        response_data = response.data.decode()
        assert response.status_code == 200
        assert '<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response_data

    def test_login(self, client):
        response = client.post('/showsummary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        assert 'Welcome' in response.data.decode()
        assert 'Simply Lift' in response.data.decode()

    def test_login_wrong_mail(self, client):
        email = 'test.fail@email.com'
        response = client.post('/showsummary', data={'email': email})
        assert response.status_code == 200
        assert 'Sorry, that email was not found' in response.data.decode()





