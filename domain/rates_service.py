from typing import List

from domain.rates_schema import MinMaxAverageSchema


class RatesService:
    @staticmethod
    def average_exchange_rate(bid_price: float, ask_price: float) -> float:
        average = (bid_price + ask_price) / 2
        return round(average, 4)

    @staticmethod
    def min_max_average_values(rates: List) -> MinMaxAverageSchema:
        min_average_value = min([element['mid'] for element in rates])
        max_average_value = max([element['mid'] for element in rates])

        return MinMaxAverageSchema(min=min_average_value, max=max_average_value)