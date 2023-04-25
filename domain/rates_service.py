import requests
from fastapi import HTTPException
from starlette import status

from domain.rates_schema import MinMaxAverageSchema
from domain.utils import check_date_format_correctness, check_currency_code_format_correctness, \
    check_quotations_correctness


class RatesService:

    @staticmethod
    def average_rate_for_date(currency_code: str, date: str):
        """
        :param currency_code: three-letter currency code as specified by NBP
        :param date: date as string formatted to YYYY-MM-DD
        :return: an average exchange rate before a provided date
        """

        check_currency_code_format_correctness(currency_code)
        check_date_format_correctness(date)

        currency_rates_json = RatesService.__download_rates_table_by_date(currency_code, date)

        return float(currency_rates_json['rates'][0]['mid'])

    @staticmethod
    def min_max_average(currency_code: str, quotations: int) -> MinMaxAverageSchema:
        """
        :param currency_code: three-letter currency code as specified by NBP
        :param quotations: number of working days before the current date to take into consideration
        :return: the maximum and minimum average value of an exchange rate
        """

        check_currency_code_format_correctness(currency_code)
        check_quotations_correctness(quotations)

        rates_table = RatesService.__download_rates_table_by_quotations(currency_code, quotations, table='a')

        min_average_value = min([element['mid'] for element in rates_table['rates']])
        max_average_value = max([element['mid'] for element in rates_table['rates']])

        return MinMaxAverageSchema(min=min_average_value, max=max_average_value)

    @staticmethod
    def major_buy_ask_difference(currency_code: str, quotations: int):
        """
        :param currency_code: three-letter currency code as specified by NBP
        :param quotations: number of working days before the current date to take into consideration
        :return: maximum absolute difference between buy and ask rates for a provided currency
        """

        check_currency_code_format_correctness(currency_code)
        check_quotations_correctness(quotations)

        rates_table = RatesService.__download_rates_table_by_quotations(currency_code, quotations, table='c')

        buy_ask_differences = [abs(round(element['bid'] - element['ask'], 4)) for element in rates_table['rates']]

        return max(buy_ask_differences)

    @staticmethod
    def __download_rates_table_by_date(currency_code: str, date: str):
        """
        :param currency_code: three-letter currency code as specified by NBP
        :param date: date as string formatted to YYYY-MM-DD
        :return: currency rate rates table in json format with single entry provided by NBP
        """
        currency_rates_response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/a/'
                                               f'{currency_code.lower()}/{date}/?format=json')
        if currency_rates_response.status_code != 200:
            raise HTTPException(status_code=currency_rates_response.status_code, detail=currency_rates_response.text)

        return currency_rates_response.json()

    @staticmethod
    def __download_rates_table_by_quotations(currency_code: str, quotations: int, table: str = 'a'):
        """
        :param currency_code: three-letter currency code as specified by NBP
        :param quotations: number of working days before the current date to take into consideration
        :param table: exchange rates table, only tables 'a' and 'c' are currently supported
        :return: chosen currency rates table by number of quotations in json format provided by NBP
        """
        if table != 'a' and table != 'c':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Exchange tables other than "a" or "c" are not supported')

        multiple_rates_response = requests.get(
            f'https://api.nbp.pl/api/exchangerates/rates/{table}/{currency_code}/last/{quotations}/?format=json')
        if multiple_rates_response.status_code != 200:
            raise HTTPException(status_code=multiple_rates_response.status_code, detail=multiple_rates_response.text)

        return multiple_rates_response.json()
