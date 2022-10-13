import io
import json

import requests
import xmltodict
from fastapi.encoders import jsonable_encoder

from models import RatePrice
from redis_client import RedisClient


class Pricer:
    def __init__(self, bank_url: str = "https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021"):
        self.bank_url = bank_url
        self.rate_prices = None
        self.redis_key = "prices"

    def update_rates(self):
        response_data = self.send_request()
        self.get_rate_prices(response_data)
        return jsonable_encoder(self.rate_prices)

    def send_request(self) -> dict:
        with requests.Session() as session:
            xml_response = session.get(url=self.bank_url)
            return xmltodict.parse(xml_response.content)

    def get_rate_prices(self, response_data: dict):
        items = response_data.get("rates", {}).get("item", {})
        if items:
            self.rate_prices = [RatePrice(**item) for item in items]

    def set_prices_from_db(self):
        if self.rate_prices is None:
            response = RedisClient().get(key=self.redis_key)
            if response is None:
                return
            fix_bytes_value = response.replace(b"'", b'"')
            my_json = json.load(io.BytesIO(fix_bytes_value))
            self.rate_prices = {element["title"]: RatePrice(**element) for element in my_json}
