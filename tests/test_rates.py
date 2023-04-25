from fastapi.testclient import TestClient

from api.api import app

test_client = TestClient(app)


def test_average_rate_for_date_dkk():
    response = test_client.get('/rates/dkk/average/2023-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': 0.6279
    }


def test_average_rate_for_date_usd():
    response = test_client.get('/rates/usd/average/2016-04-04')

    assert response.status_code == 200
    assert response.json() == {
        'average_rate': 3.7254
    }


def test_average_rate_for_date_bad_currency_code():
    response = test_client.get('/rates/abcd/average/2016-04-04')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Currency code: abcd in wrong format'}


def test_average_rate_for_date_bad_date_format():
    response = test_client.get('/rates/usd/average/04-04-2021')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Date: 04-04-2021 in wrong format, use YYYY-MM-DD'}


def test_average_rate_for_date_nonexistent_currency():
    response = test_client.get('/rates/pln/average/2023-04-04')

    assert response.status_code == 404
    assert response.json() == {'detail': '404 NotFound - Not Found - Brak danych'}


def test_min_max_average_exchange_rate_sek():
    response = test_client.get('/rates/sek/min-max-average/30')

    assert response.status_code == 200
    assert response.json() == {
        'min_average_value': 0.4059,
        'max_average_value': 0.4231
    }


def test_min_max_average_exchange_rate_czk():
    response = test_client.get('/rates/czk/min-max-average/20')

    assert response.status_code == 200
    assert response.json() == {
        'min_average_value': 0.1955,
        'max_average_value': 0.2002
    }


def test_min_max_average_exchange_rate_bad_currency_code():
    response = test_client.get('/rates/qqqq/min-max-average/30')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Currency code: qqqq in wrong format'}


def test_min_max_average_exchange_rate_bad_number_of_quotations():
    response = test_client.get('/rates/czk/min-max-average/500')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Quotations exceed the <1, 255> range'}


def test_min_max_average_exchange_rate_wrong_date():
    response = test_client.get('/rates/czk/average/2023-04-56')

    assert response.status_code == 404
    assert response.json() == {'detail': '\ufeff404 NotFound'}


def test_major_buy_ask_difference_sek():
    response = test_client.get('/rates/sek/buy-ask-difference/20')

    assert response.status_code == 200
    assert response.json() == {'major_buy_ask_difference': 0.0084}


def test_major_buy_ask_difference_usd():
    response = test_client.get('/rates/usd/buy-ask-difference/30')

    assert response.status_code == 200
    assert response.json() == {'major_buy_ask_difference': 0.089}


def test_major_buy_ask_difference_bad_currency_code_format():
    response = test_client.get('/rates/zz/buy-ask-difference/30')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Currency code: zz in wrong format'}


def test_major_buy_ask_difference_bad_number_of_quotations_too_high():
    response = test_client.get('/rates/usd/buy-ask-difference/512')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Quotations exceed the <1, 255> range'}


def test_major_buy_ask_difference_bad_number_of_quotations_too_low():
    response = test_client.get('/rates/usd/buy-ask-difference/0')

    assert response.status_code == 400
    assert response.json() == {'detail': 'Quotations exceed the <1, 255> range'}