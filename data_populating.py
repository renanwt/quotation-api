import requests
from datetime import datetime, timedelta, date
import time

BASE_URL = "http://quotation-api-iljn.onrender.com/api/records/"
# BASE_URL = "http://localhost:8000/api/records/"


def make_request(quotation_date):
    url = BASE_URL
    payload = {"quotation_date": quotation_date}
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        print(f"Request successful for date: {quotation_date}")
    else:
        print(f"Request failed for date: {quotation_date}, Status code: {response.status_code}")


def main():
    # Set the initial date
    current_date = datetime.strptime("2024-02-13", "%Y-%m-%d")

    # Run the loop until a certain date
    while current_date >= datetime.strptime("2010-01-01", "%Y-%m-%d"):
        # Format the current date
        formatted_date = current_date.strftime("%Y-%m-%d")

        # Make the request
        make_request(formatted_date)

        # Decrement the date by one day
        current_date -= timedelta(days=1)

        # Wait for 5 seconds
        time.sleep(1)


if __name__ == "__main__":
    main()
