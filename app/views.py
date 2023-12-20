from rest_framework import generics
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer


class FinancialRecordList(generics.ListCreateAPIView):
    serializer_class = FinancialRecordSerializer

    def get_queryset(self):
        queryset = FinancialRecord.objects.all()
        starting_date = self.request.query_params.get('starting_date')
        if starting_date is not None:
            queryset = queryset.filter(create_date=starting_date)
        return queryset

