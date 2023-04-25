from fastapi.testclient import TestClient

from api.api import app

test_client = TestClient(app)


def test_average_rate_for_date_1():
    response = test_client.get('/rates/dkk/average/2023-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': '0.6279'
    }


def test_average_rate_for_date_2():
    response = test_client.get('/rates/usd/average/2016-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': '3.7254'
    }
