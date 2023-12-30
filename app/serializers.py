from rest_framework import serializers
from .models import FinancialRecord


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FinancialRecordDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = ['date', 'brl', 'usd', 'eur', 'jpy']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fields = self.context.get('fields')

        if fields:
            ordered_fields = ['date'] + fields
            return {field: data[field] for field in ordered_fields}

        return data
