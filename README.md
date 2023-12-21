# Quotation API

Welcome to quotation API.

To run the APP
(Windows) execute:
>python manage.py runserver

To test:
>python manage.py test app

## Use the Postman Collection Attached to execute the API.

****
## Endpoints for local tests

>[GET] http://127.0.0.1:8000/api/records/
>
> Not required Query Params (examples):
>>"start_date": "2023-12-11"
>>
>>  "end_date": "2023-12-10"
>>
>>  "currency": "brl"
 
> [POST] http://127.0.0.1:8000/api/records
>>
>>Request Body:
>>
>>{ "quotation_date": "2023-11-12" }