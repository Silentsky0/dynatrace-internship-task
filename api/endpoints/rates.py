from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from domain.rates_service import RatesService

router = FastAPI()


@router.get('/{currency_code}/average/{date}')
async def average_exchange_rate_for_date(currency_code: str, date: str):
    """
    Returns an average exchange rate before a provided date
    """

    average_rate = RatesService.average_rate_for_date(currency_code, date)

    return {'average_rate': average_rate}


@router.get('/{currency_code}/min-max-average/{quotations}')
async def min_max_average_exchange_rate(currency_code: str, quotations: int):
    """
    Returns the maximum and minimum average value of an exchange rate
    """
    min_max_average_values = RatesService.min_max_average(currency_code, quotations)

    return {'min_average_value': min_max_average_values.min, 'max_average_value': min_max_average_values.max}


@router.get('/{currency_code}/buy-ask-difference/{quotations}')
async def major_buy_ask_difference(currency_code: str, quotations: int):
    """
    Returns the maximum absolute difference between buy and ask rates for a provided currency
    """

    major_buy_ask_difference_value = RatesService.major_buy_ask_difference(currency_code, quotations)

    return {'major_buy_ask_difference': major_buy_ask_difference_value}
