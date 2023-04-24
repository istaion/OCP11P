from tests.config import client, mock_data
import pytest


@pytest.mark.usefixtures('client', 'mock_data')
class TestInteg:
    def test_purchase_place(self, client):
        # check if points of Simply Lift is 13
        response = client.get('/show_points')
        assert "<td>Simply Lift</td>\n                <td>13</td>" in response.data.decode()
        # check if places of Spring Festival is 25
        response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
        assert 'Spring Festival<br />\n            Date: 2025-03-27 10:00:00</br>\n            Number of Places: 25' \
               in response.data.decode()
        # book 1 place and check response status code and root
        response = client.post('/purchase_places', data={'club': 'Simply Lift',
                                                         'competition': 'Spring Festival', 'places': '1'
                                                         }
                               )
        assert response.status_code == 200
        assert 'Great-booking complete!' in response.data.decode()
        # check if points correctly deducted
        response = client.get('/show_points')
        assert "<td>Simply Lift</td>\n                <td>12</td>" in response.data.decode()
        # check if places correctly deducted
        response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
        assert 'Spring Festival<br />\n            Date: 2025-03-27 10:00:00</br>\n            Number of Places: 24' \
               in response.data.decode()

    def test_wrong_purchase_place(self, client):
        # check if points of Iron Temple is 4
        response = client.get('/show_points')
        assert "<td>Iron Temple</td>\n                <td>4</td>" in response.data.decode()
        # check if places of Spring Festival is 25 and 13 for Fall classic
        response = client.post('/show_summary', data={'email': 'admin@irontemple.com'})
        assert 'Spring Festival<br />\n            Date: 2025-03-27 10:00:00</br>\n            Number of Places: 25' \
               in response.data.decode()
        assert 'Fall Classic<br />\n            Date: 2020-10-22 13:30:00</br>\n            Number of Places: 13' \
               in response.data.decode()
        # try to book 13 place and check response status code and root
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'Spring Festival', 'places': '13'
                                                         }
                               )
        assert response.status_code == 200
        assert 'book more than 12 points' in response.data.decode()
        # try to book 5 place and check response status code and root
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'Spring Festival', 'places': '5'
                                                         }
                               )
        assert response.status_code == 200
        assert 'have enough points' in response.data.decode()
        # try to book for a past competition and check response status code and root
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'Fall Classic', 'places': '2'
                                                         }
                               )
        assert response.status_code == 200
        assert 'book for a past competition' in response.data.decode()
        # try to book more than free place
        response = client.post('/purchase_places', data={'club': 'Iron Temple',
                                                         'competition': 'test place', 'places': '11'
                                                         }
                               )
        assert response.status_code == 200
        assert 'No enough places' in response.data.decode()
