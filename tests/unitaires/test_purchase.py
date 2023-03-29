from tests.config import client
import pytest


@pytest.mark.usefixtures("client")
class Tests:
    def test_purchasePlaces(self, client):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': '1'
                                                        }
                               )
        assert response.status_code == 200
        assert 'Great-booking complete!' in response.data.decode()

    def test_purchasePlaces_past_competition(self, client):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Fall Classic',
                                                        'places': 1})
        assert response.status_code == 200
        assert 'book for a past competition' in response.data.decode()

    def test_purchasePlaces_more_than_12(self, client):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': '13'
                                                        }
                               )
        assert response.status_code == 200
        assert 'book more than 12 points' in response.data.decode()

    def test_purchasePlaces_not_enought_points(self, client):
        response = client.post('/purchasePlaces', data={'club': 'Iron Temple',
                                                        'competition': 'Spring Festival',
                                                        'places': '7'
                                                        }
                               )
        assert response.status_code == 200
        assert 'have enough points' in response.data.decode()



