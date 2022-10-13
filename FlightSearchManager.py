import json
from typing import Optional, List

from fastapi.encoders import jsonable_encoder

from Pricer import Pricer
from models import Flights, Price


class FlightSearchManager:
    def __init__(self, file_path='response_a.json'):
        self.file_path = file_path
        self.pricer = Pricer()

    @staticmethod
    def sort(updated_flights: Optional[List[Flights]]) -> List[Flights]:
        return sorted(updated_flights, key=lambda x: x.price.amount, reverse=True)

    @classmethod
    def get_flights_from_json(cls, json_data: dict) -> dict:
        flights = [Flights(**element) for element in json_data]
        return jsonable_encoder(flights)

    def update_and_sort(self, flights: Optional[List[Flights]], input_currency: str):
        flights = [Flights(**element) for element in flights]
        updated_flights, is_updated = self.update_price(flights, input_currency)
        return jsonable_encoder(self.sort(updated_flights)), is_updated

    def update_price(self, flights: List[Flights], input_currency: str):
        self.pricer.set_prices_from_db()
        if self.pricer.rate_prices is None:
            return flights, False
        for element in flights:
            currency = element.pricing.currency
            total = element.pricing.total
            if currency == input_currency:
                element.price = Price(**
                                      {"amount": total, "currency": input_currency})
            else:
                rate = self.pricer.rate_prices.get(currency, None)
                if rate:
                    element.price = Price(**
                                          {"amount": "{:.2f}".format(rate.description / rate.quant * total),
                                           "currency": input_currency})
        return flights, True

    def search_flights(self) -> dict:
        json_data = self.upload_json_from_file()
        flights = self.get_flights_from_json(json_data)
        return flights

    def upload_json_from_file(self) -> dict:
        with open(file=self.file_path) as json_file:
            json_data = json.load(json_file)
            return json_data
