from django.db import models
from datetime import date


class FinancialRecord(models.Model):
    usd = models.DecimalField(max_digits=10, decimal_places=2)
    brl = models.DecimalField(max_digits=10, decimal_places=2)
    eur = models.DecimalField(max_digits=10, decimal_places=2)
    jpy = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today(), unique=True)

    def __str__(self):
        return f"Financial Record - {self.date}"
