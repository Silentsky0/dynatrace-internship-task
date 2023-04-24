
class RatesService:
    @staticmethod
    def average_exchange_rate(bid_price: float, ask_price: float):
        average = (bid_price + ask_price) / 2
        return round(average, 4)
