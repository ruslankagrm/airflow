import json
import os.path

import pytest
from fastapi.testclient import TestClient
from kombu.exceptions import OperationalError
from pydantic import ValidationError

from FlightSearchManager import FlightSearchManager
from main import airflow
from models import SearchTaskResult, Pricing

client = TestClient(airflow)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404


def test_search():
    with pytest.raises(OperationalError):
        client.post("/search")


def test_results_wrong_params():
    response = client.get("/results/22/KZT")
    assert response.status_code == 422
    assert response.json() == json.loads(
        '{"detail":[{"loc":["path","search_id"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}')


def test_serialization_from_file():
    wrong_file_path = os.path.join('not_a_file.json')
    with pytest.raises(FileNotFoundError):
        FlightSearchManager(wrong_file_path).search_flights()

    test_file_path = os.path.join('test_response.json')
    with pytest.raises(ValidationError):
        FlightSearchManager(test_file_path).search_flights()

    test_file_path = os.path.join('response_a.json')
    result = FlightSearchManager(test_file_path).search_flights()
    expected_len = 223
    assert expected_len == len(result)


def test_models_serialization():
    task_result_input_dict = {
        "search_id": 2,
        "status": "FAILED",
        "items": {}
    }
    with pytest.raises(ValidationError):
        SearchTaskResult(**task_result_input_dict)

    pricing_input_dict = {
        "total": {"1"},
        "base": 3,
    }
    with pytest.raises(ValidationError):
        Pricing(**pricing_input_dict)
