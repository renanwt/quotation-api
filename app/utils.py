from datetime import date, timedelta

import requests


def dollar_to_all(date_ref):
    api_endpoint = f'https://api.vatcomply.com/rates?date={date_ref}&base=USD'
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()

        dollar_quotation = {
            'BRL': round(data['rates']['BRL'], 2),
            'EUR': round(data['rates']['EUR'], 2),
            'JPY': round(data['rates']['JPY'], 2)
        }
        return dollar_quotation
    else:
        return None


def date_validator(start_date_param, end_date_param):
    if start_date_param and end_date_param:
        start_date = date.fromisoformat(str(start_date_param))
        end_date = date.fromisoformat(str(end_date_param))
        if (end_date - start_date).days >= 5 or end_date < start_date:
            return False
        else:
            return True
    else:
        return True


def date_autodata(start_date_param, end_date_param):
    start_date = end_date = ''
    if start_date_param and end_date_param:
        start_date = start_date_param
        end_date = end_date_param
    elif start_date_param:
        start_date = date.fromisoformat(str(start_date_param))
        end_date = start_date + timedelta(days=4)
    elif end_date_param:
        end_date = date.fromisoformat(str(end_date_param))
        start_date = end_date - timedelta(days=4)
    date_data = {
        'start_date': start_date,
        'end_date': end_date
    }
    return date_data


def currency_validator(currency):
    if currency.lower() in ['brl', 'usd', 'eur', 'jpy']:
        return True
    else:
        return False
