from rest_framework import generics, status
from rest_framework.response import Response
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer, FinancialRecordGetAllSerializer, FinancialRecordGetBRLSerializer, \
    FinancialRecordGetEURSerializer, FinancialRecordGetJPYSerializer
from .utils import dollar_to_all, date_validator, currency_validator
from datetime import date, timedelta


class FinancialRecordList(generics.GenericAPIView):
    serializer_class = FinancialRecordSerializer
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
            # Creating Record
            record = FinancialRecord.objects.create(
                brl=brl_value,
                usd=usd_value,
                eur=eur_value,
                jpy=jpy_value,
                date=quotation_date
            )
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                return Response(f"This date quotation is already recorded.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"Failed saving quotation: {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = FinancialRecordSerializer(data=record.__dict__)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        start_date_param = request.query_params.get('start_date', '')
        end_date_param = request.query_params.get('end_date', date.today())
        currency_param = request.query_params.get('currency', None)

        start_date = end_date = None

        if currency_param and not currency_validator(currency_param):
            return Response("Not valid currency. It must be: 'brl', 'eur' or 'jpy'.",
                            status=status.HTTP_400_BAD_REQUEST)

        if start_date_param and end_date_param:
            if not date_validator(start_date_param, end_date_param):
                return Response("Difference between end_date and start_date should be at most 5 days.",
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                start_date = start_date_param
                end_date = end_date_param
        else:
            if start_date_param:
                start_date = date.fromisoformat(str(start_date_param))
                end_date = start_date + timedelta(days=4)
            else:
                end_date = date.fromisoformat(str(end_date_param))
                start_date = end_date - timedelta(days=4)
        try:
            if not currency_param:
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date)))
                serializer = FinancialRecordGetAllSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif currency_param.lower() == 'brl':
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date)))
                serializer = FinancialRecordGetBRLSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif currency_param.lower() == 'eur':
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date)))
                serializer = FinancialRecordGetEURSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif currency_param.lower() == 'jpy':
                queryset = FinancialRecord.objects.filter(date__range=(str(start_date), str(end_date)))
                serializer = FinancialRecordGetJPYSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif currency_param.lower() == 'usd':
                return Response("USD quotation in USD is 1.00. Please try 'BRL', 'EUR' or 'JPY'.",
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Failed getting quotation: {e}", status=status.HTTP_400_BAD_REQUEST)
