import json
from typing import Optional, List

from models import Flights


class FlightSearchManager:
    def __init__(self, file_path='response_a.json'):
        self.file_path = file_path

    async def search_flights(self):
        data = self.upload_json_from_file()
        flights = await FlightSearchManager().get_flights_from_json(data)
        return flights

    def upload_json_from_file(self):
        with open(file=self.file_path) as json_file:
            json_data = json.load(json_file)
            return json_data

    @classmethod
    async def get_flights_from_json(cls, json_data: Optional[List[Flights]]):
        flights = [Flights(**element) for element in json_data]
        return flights
