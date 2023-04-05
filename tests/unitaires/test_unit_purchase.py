from tests.config import client, mock_data
import pytest


@pytest.mark.usefixtures("client")
class Tests:
    def test_purchase_places(self, client, mock_data):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': '1'
                                                        }
                               )
        assert response.status_code == 200
        assert 'Great-booking complete!' in response.data.decode()
        club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
        assert club['points'] == '12'

    def test_purchase_places_past_competition(self, client, mock_data):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Fall Classic',
                                                        'places': '1'})
        assert response.status_code == 200
        assert 'book for a past competition' in response.data.decode()

    def test_purchase_places_more_than_12(self, client, mock_data):
        response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': '13'
                                                        }
                               )
        assert response.status_code == 200
        assert 'book more than 12 points' in response.data.decode()

    def test_purchase_places_not_enough_points(self, client, mock_data):
        response = client.post('/purchasePlaces', data={'club': 'Iron Temple',
                                                        'competition': 'Spring Festival',
                                                        'places': '7'
                                                        }
                               )
        assert response.status_code == 200
        assert 'have enough points' in response.data.decode()

    def test_purchase_places_not_enough_place(self, client, mock_data):
        response = client.post('/purchasePlaces', data={'club': 'Iron Temple',
                                                        'competition': 'Spring Festival',
                                                        'places': '7'
                                                        }
                               )
        assert response.status_code == 200
        assert 'have enough points' in response.data.decode()



