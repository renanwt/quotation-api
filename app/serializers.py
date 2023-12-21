from rest_framework import serializers
from .models import FinancialRecord


class FinancialRecordGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'usd', 'brl', 'eur', 'jpy']


class FinancialRecordGetBRLSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'brl']


class FinancialRecordGetEURSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'eur']


class FinancialRecordGetJPYSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'jpy']
