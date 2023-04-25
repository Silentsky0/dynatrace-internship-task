from fastapi.testclient import TestClient

from api.api import app

test_client = TestClient(app)


def test_average_rate_for_date_dkk():
    response = test_client.get('/rates/dkk/average/2023-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': '0.6279'
    }


def test_average_rate_for_date_usd():
    response = test_client.get('/rates/usd/average/2016-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': '3.7254'
    }


def test_average_rate_for_date_bad_currency_code():
    response = test_client.get('/rates/abcd/average/2016-04-04')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Currency code: abcd in wrong format'}


def test_average_rate_for_date_bad_date_format():
    response = test_client.get('/rates/usd/average/04-04-2021')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Date: 04-04-2021 in wrong format, use YYYY-MM-DD'}
