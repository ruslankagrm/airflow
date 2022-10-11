import uuid

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from providers import create_task

description = """
## Airflow API helps you to get an info about the flight🚀

### Utility
You are able to get needed flights' info

"""
airflow = FastAPI(
    title="Airflow",
    description=description,
    version="0.0.1",
)


@airflow.get("/results/{search_id}",
             description="### This endpoint is to search the flight info",
             status_code=200,
             )
async def results(search_id: str):
    search_result = AsyncResult(search_id)
    result = {
        "search_id": search_id,
        "status": search_result.status,
        "items": search_result.result
    }
    return JSONResponse(result)


@airflow.post("/search",
              description="### This endpoint will start the search and give you a unique id, which you can use to get a detailed info",
              status_code=201,
              )
async def search():
    search_task = create_task.delay()
    return JSONResponse({"search_id": search_task.id})
