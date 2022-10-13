# Airflow APP

### Utility:
You can get detailed information about flight

You will get JSON info representation, flights are sorted for currency you choose

___
### Setup:

1) To run an application you should have 🐳 **docker** and **docker-compose** installed.
2) Run the following commands in terminal:
   ```
   1) docker-compose -f docker-compose.yaml build
   2) docker-compose -f docker-compose.yaml up
    ```
3) Now you are ready to start 🚀
4) Your server is running, check swagger page to test an app functionality
on ```localhost:9000/docs```

## API Reference

#### Create an announcement 

```http
  POST /search
```

| Response | Type   | Description                                                                                                                     |
|:---------|:-------|:--------------------------------------------------------------------------------------------------------------------------------|
| `Status` | `int`  | 201 - Successfully created a search task                                                                                        |
| `Body`   | `json` | You will get json response like this, search_id you will use to get results<br/> <br/>"```search_id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"``` |


#### Get detailed info about flights

```http
  GET /results/{search_id}/{currency}
```
#### Response example
| Parameter | Type   | Description                                                |
|:---------|:-------|:-----------------------------------------------------------|
| `search_id`    | `uuid` | Search id you got from the **search** method               |
 `currency`    | `str`  | What currency you whant prcices to be converted and sorted |

Documentation is available on `/docs` or `/redoc`
