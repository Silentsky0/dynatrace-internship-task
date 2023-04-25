import datetime
import re

import requests
from fastapi import FastAPI, HTTPException
from starlette import status

from domain.rates_service import RatesService

router = FastAPI()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get('/{currency_code}/average/{date}')
async def average_rate_for_date(currency_code: str, date: str):
    """
    :param currency_code: three-letter currency code as specified by NBP
    :param date: date as string formatted to YYYY-MM-DD
    :return: an average exchange rate before a provided date
    """

    average_rate = RatesService.average_rate_for_date(currency_code, date)

    return {'average_rate': f'{average_rate}'}


@router.get('/{currency_code}/min-max-average/{quotations}')
async def max_min_average(currency_code: str, quotations: int):
    """
    :param currency_code: three-letter currency code as specified by NBP
    :param quotations: number of working days before the current date to take into consideration
    :return: the maximum and minimum average value of an exchange rate
    """
    min_max_average_values = RatesService.min_max_average(currency_code, quotations)

    return {'min-average-value': min_max_average_values.min, 'max-average-value': min_max_average_values.max}


@router.get('/{currency_code}/buy-ask-difference/{quotations}')
async def buy_ask_difference(currency_code: str, quotations: int):
    """
    :param currency_code: three-letter currency code as specified by NBP
    :param quotations: number of working days before the current date to take into consideration
    :return: maximum absolute difference between buy and ask rates for a provided currency
    """

    major_buy_ask_difference = RatesService.major_buy_ask_difference(currency_code, quotations)

    return {'major-buy-ask-difference': major_buy_ask_difference}
