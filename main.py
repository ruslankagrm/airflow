import uuid

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from FlightSearchManager import FlightSearchManager
from models import SearchTaskResult
from tasks import get_tasks_result, create_search_tasks

description = """
## Airflow API helps you to get an info about the flight🚀

### Utility
You can get detailed information about flight

You will get JSON info representation, flights are sorted for currency you choose
"""
airflow = FastAPI(
    title="Airflow",
    description=description,
    version="0.0.1",
)


@airflow.get("/results/{search_id}/{currency}",
             description="### This endpoint is to search the flight info",
             status_code=200,
             )
async def results(search_id: uuid.UUID, currency: str = "KZT") -> JSONResponse:
    search_tasks_result = get_tasks_result(search_id=str(search_id))
    if search_tasks_result.status == "SUCCESS":
        flights_info, flag = FlightSearchManager().update_and_sort(flights=search_tasks_result.items,
                                                                   input_currency=currency)
        if flag:
            search_tasks_result.items = flights_info
    return JSONResponse(search_tasks_result.to_json_response())


@airflow.post("/search",
              description="### This endpoint will start the search and give you a unique id, which you can use to get a detailed info",
              status_code=201,
              )
async def search() -> JSONResponse:
    search_task = create_search_tasks.delay()
    search_task_result = SearchTaskResult(**{"search_id": search_task.id})
    return JSONResponse(search_task_result.status_response())
