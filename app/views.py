from django.shortcuts import render
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from .models import FinancialRecord
from .serializers import FinancialRecordGetAllSerializer, FinancialRecordGetBRLSerializer, \
    FinancialRecordGetEURSerializer, FinancialRecordGetJPYSerializer
from .utils import dollar_to_all, date_validator, currency_validator, date_autodata
from datetime import date

API_URL = 'http://quotation-api-iljn.onrender.com/api/records/'


class FinancialRecordGetPostView(generics.GenericAPIView):
    serializer_class = FinancialRecordGetAllSerializer
    queryset = FinancialRecord.objects.all()

    def post(self, request):
        quotation_date = request.data.get('quotation_date', date.today())

        try:
            quotation = dollar_to_all(quotation_date)
            if not quotation:
                return Response("Failed getting quotation.", status=status.HTTP_404_NOT_FOUND)
            else:
                usd_value = 1
                brl_value = quotation['BRL']
                eur_value = quotation['EUR']
                jpy_value = quotation['JPY']
        except Exception as e:
            return Response(f"Failed getting quotation: {e}", status=status.HTTP_404_NOT_FOUND)

        try:
            if self.queryset.filter(date=quotation_date):
                return Response(f"This date quotation is already recorded.", status=status.HTTP_400_BAD_REQUEST)

            # Creating Record
            record = FinancialRecord.objects.create(
                brl=brl_value,
                usd=usd_value,
                eur=eur_value,
                jpy=jpy_value,
                date=quotation_date
            )
        except Exception as e:
            return Response(f"Failed saving quotation: {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=record.__dict__)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        start_date_param = request.query_params.get('start_date', '')
        end_date_param = request.query_params.get('end_date', '')
        currency_param = request.query_params.get('currency', None)

        if currency_param and not currency_validator(currency_param):
            return Response("Not valid currency. It must be: 'brl', 'eur' or 'jpy'.",
                            status=status.HTTP_400_BAD_REQUEST)

        if not date_validator(start_date_param, end_date_param):
            if not date_validator(start_date_param, end_date_param):
                return Response("Difference between end_date and start_date should be between 0 and 5 days.",
                                status=status.HTTP_400_BAD_REQUEST)

        date_data = date_autodata(start_date_param, end_date_param)
        start_date = date_data['start_date']
        end_date = date_data['end_date']

        try:
            if not currency_param:
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date))).order_by('date')
                serializer_class = self.serializer_class
            elif currency_param.lower() == 'usd':
                return Response("USD quotation in USD is 1.00. Please try 'BRL', 'EUR' or 'JPY'.",
                                status=status.HTTP_200_OK)
            else:
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date))).order_by('date')
                serializer_class = {
                    'brl': FinancialRecordGetBRLSerializer,
                    'eur': FinancialRecordGetEURSerializer,
                    'jpy': FinancialRecordGetJPYSerializer,
                }.get(currency_param.lower(), None)

                if serializer_class is None:
                    return Response("Invalid currency parameter.", status=status.HTTP_400_BAD_REQUEST)

            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(f"Failed getting quotation: {e}", status=status.HTTP_400_BAD_REQUEST)


class HighchartsView(generics.GenericAPIView):

    def get(self, request):
        start_date = request.query_params.get('start_date', '')
        end_date = request.query_params.get('end_date', '')
        currency_param = request.query_params.get('currency', None)

        if currency_param and not currency_validator(currency_param):
            return Response("Not valid currency. It must be: 'brl', 'eur' or 'jpy'.",
                            status=status.HTTP_400_BAD_REQUEST)

        if not date_validator(start_date, end_date):
            return Response("Difference between end_date and start_date should be between 0 and 5 days.",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(API_URL,
                                    params={'start_date': start_date, 'end_date': end_date, 'currency': currency_param})
            response.raise_for_status()
        except Exception as e:
            return Response(f"Failed getting quotation: {e}", status=status.HTTP_400_BAD_REQUEST)

        try:
            if response.status_code == 200:
                financial_data = response.json()
                return render(request, 'index.html', {'chart_data': financial_data})
        except Exception as e:
            return Response(f"Failed to get financial data charts: {e}", status=status.HTTP_400_BAD_REQUEST)
