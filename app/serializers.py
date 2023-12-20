from rest_framework import serializers
from .models import FinancialRecord


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = '__all__'


class FinancialRecordGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'brl', 'eur', 'jpy']


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
