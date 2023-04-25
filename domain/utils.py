import re

from fastapi import HTTPException
from starlette import status


def check_currency_code_format_correctness(currency_code: str):
    currency_code_regex = re.compile('^[a-zA-Z]{3}$')
    if not currency_code_regex.match(currency_code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Currency code: {currency_code} in wrong format')


def check_date_format_correctness(date: str):
    date_format_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    if not date_format_regex.match(date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Date: {date} in wrong format, use YYYY-MM-DD')


def check_quotations_correctness(quotations: int):
    if quotations > 255:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Quotations exceed the <0, 255> range')
