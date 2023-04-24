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
async def average_rates_for_date(currency_code: str, date: str):

    # check that code and date formats are correct
    currency_code_regex = re.compile('^[a-zA-Z]{3}$')
    if not currency_code_regex.match(currency_code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Currency code: {currency_code} in wrong format')

    date_format_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    if not date_format_regex.match(date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Date: {date} in wrong format, use YYYY-MM-DD')

    currency_rates_response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/'
                                           f'{currency_code.lower()}/{date}/?format=json')
    if currency_rates_response.status_code != 200:
        raise HTTPException(status_code=currency_rates_response.status_code, detail=currency_rates_response.text)

    currency_rates_json = currency_rates_response.json()

    average_rate = RatesService.average_exchange_rate(currency_rates_json['rates'][0]['bid'],
                                                      currency_rates_json['rates'][0]['ask'])

    return {'average_rate': f'{average_rate}'}


@router.get('/{currency_code}/max-min-average/{quotations}')
async def max_min_average(currency_code: str, quotations: int):

    currency_code_regex = re.compile('^[a-zA-Z]{3}$')
    if not currency_code_regex.match(currency_code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Currency code: {currency_code} in wrong format')

    # check quotations format

    multiple_rates_response = requests.get(
        f'https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/last/{quotations}/?format=json')
    if multiple_rates_response.status_code != 200:
        raise HTTPException(status_code=multiple_rates_response.status_code, detail=multiple_rates_response.text)

    rates_table = multiple_rates_response.json()['rates']

    min_max_average_values = RatesService.min_max_average_values(rates_table)

    return {'max-average-value': min_max_average_values.max, 'min-average-value': min_max_average_values.min}
