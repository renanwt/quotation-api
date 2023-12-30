from datetime import date
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FinancialRecord
import unittest.mock


class FinancialRecordListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_successful(self):
        data = {'quotation_date': date.today()}
        response = self.client.post('/api/records/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FinancialRecord.objects.exists())
        self.assertEqual(FinancialRecord.objects.count(), 1)

        record = FinancialRecord.objects.first()
        self.assertEqual(record.usd, 1)

    def test_post_failed_quotation(self):
        data = {'quotation_date': date.today()}
        with unittest.mock.patch('app.views.dollar_to_all', side_effect=Exception("Failed getting quotation.")):
            response = self.client.post('/api/records/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(FinancialRecord.objects.exists())

    def test_post_failed_save_quotation(self):
        data = {'quotation_date': date.today()}
        with unittest.mock.patch('app.views.FinancialRecord.objects.create',
                                 side_effect=Exception("Failed saving quotation.")):
            response = self.client.post('/api/records/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(FinancialRecord.objects.exists())

    def test_post_duplicate_quotation(self):
        data = {'quotation_date': date.today()}
        FinancialRecord.objects.create(brl=1, usd=1, eur=1, jpy=1, date=date.today())

        response = self.client.post('/api/records/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "This date quotation is already recorded.")

    def test_get_successful(self):
        FinancialRecord.objects.create(brl=1, usd=1, eur=1, jpy=1, date=date.today())

        response = self.client.get('/api/records/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_invalid_currency(self):
        response = self.client.get('/api/records/', {'currency': 'abc'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Not valid currency. It must be: 'brl', 'eur' or 'jpy'. One or more separate " +
                                        "by comma.")

    def test_get_usd_quotation(self):
        response = self.client.get('/api/records/', {'currency': 'usd'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "USD quotation in USD is 1.00. Please try 'brl', 'eur' or 'jpy'.")

    def test_get_successful_with_currency(self):
        FinancialRecord.objects.create(brl=1, usd=1, eur=1, jpy=1, date=date.today())

        response = self.client.get('/api/records/', {'currency': 'brl'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_failed_quotation(self):
        with unittest.mock.patch('app.views.FinancialRecord.objects.filter',
                                 side_effect=Exception("Failed getting quotation.")):
            response = self.client.get('/api/records/', {'start_date': date.today(), 'end_date': date.today()})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HighchartsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_highcharts_view_invalid_currency(self):
        response = self.client.get('/api/chart/', {'currency': 'abc'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Not valid currency. It must be: 'brl', 'eur' or 'jpy'. " +
                                        "One or more separate by comma.")

    def test_highcharts_view_invalid_date_range(self):
        response = self.client.get('/api/chart/', {'start_date': '2022-01-01', 'end_date': '2022-01-08'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Difference between end_date and start_date should be between 0 and 5 days.")
