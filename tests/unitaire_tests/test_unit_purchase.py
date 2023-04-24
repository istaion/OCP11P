from tests.config import client, mock_data
import pytest


@pytest.mark.usefixtures('client', 'mock_data')
class TestsUnitPurchase:
    def test_purchase_places(self, client):
        response = client.post('/purchase_places', data={'club': 'Simply Lift',
                                                         'competition': 'Spring Festival', 'places': '1'
                                                         }
                               )
        assert response.status_code == 200
        assert 'Great-booking complete!' in response.data.decode()

    def test_purchase_places_past_competition(self, client):
        response = client.post('/purchase_places', data={'club': 'Simply Lift', 'competition': 'Fall Classic',
                                                         'places': '1'})
        assert response.status_code == 200
        assert 'book for a past competition' in response.data.decode()

    def test_purchase_places_more_than_12(self, client):
        response = client.post('/purchase_places', data={'club': 'Simply Lift',
                                                         'competition': 'Spring Festival', 'places': '13'
                                                         }
                               )
        assert response.status_code == 200
        assert 'book more than 12 points' in response.data.decode()

    def test_purchase_places_not_enough_points(self, client):
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'Spring Festival',
                                                         'places': '7'
                                                         }
                               )
        assert response.status_code == 200
        assert 'have enough points' in response.data.decode()

    def test_purchase_places_not_enough_place(self, client):
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'test place',
                                                         'places': '11'
                                                         }
                               )
        assert response.status_code == 200
        assert 'No enough places' in response.data.decode()
