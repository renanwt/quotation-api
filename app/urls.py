from django.urls import path
from .views import FinancialRecordGetPostView, HighchartsView

urlpatterns = [
    path('records/', FinancialRecordGetPostView.as_view(), name='get-post-records'),
    path('chart/', HighchartsView.as_view(), name='chart-view'),
]
