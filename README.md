# Quotation API 💻📈

Here you can Post Quotations based in a date. And collect USD quotations in JPY, BRL, EUR.
Check the rules below.

Welcome to quotation API.

To run the API locally
(Windows) execute:
>python manage.py runserver

To run local tests:
>python manage.py test app

## Use the Postman Collection Attached to execute the API.

****
## Dev Endpoints for local tests

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

> [GET] http://127.0.0.1:8000/api/chart
>
> Not required Query Params (examples):
>>"start_date": "2023-12-11"
>>
>>  "end_date": "2023-12-10"
>>
>>  "currency": "brl"

## Production Endpoints:
>> [ GET, POST ]  https://quotation-api-iljn.onrender.com/api/records
>
>> [ GET ]  https://quotation-api-iljn.onrender.com/api/records
