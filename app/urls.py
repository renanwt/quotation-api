from django.urls import path
from .views import FinancialRecordList

urlpatterns = [
    path('records/', FinancialRecordList.as_view()),
]
