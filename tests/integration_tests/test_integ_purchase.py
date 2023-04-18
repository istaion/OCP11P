from tests.config import client, mock_data
import pytest


@pytest.mark.usefixtures('client', 'mock_data')
def test_purchase_place(client):
    # check if points of Simply Lift is 13
    response = client.get('/showPoints')
    assert "<td>Simply Lift</td>\n                <td>13</td>" in response.data.decode()
    # check if places of Spring Festival is 25
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert 'Spring Festival<br />\n            Date: 2025-03-27 10:00:00</br>\n            Number of Places: 25' \
           in response.data.decode()
    # book 1 place and check response status code and root
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                    'competition': 'Spring Festival', 'places': '1'
                                                    }
                           )
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode()
    # check if points correctly deducted
    response = client.get('/showPoints')
    assert "<td>Simply Lift</td>\n                <td>12</td>" in response.data.decode()
    # check if places correctly deducted
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert 'Spring Festival<br />\n            Date: 2025-03-27 10:00:00</br>\n            Number of Places: 24' \
           in response.data.decode()
