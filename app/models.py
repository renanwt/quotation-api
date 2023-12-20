from django.db import models


class FinancialRecord(models.Model):
    usd = models.DecimalField(max_digits=10, decimal_places=2)
    brl = models.DecimalField(max_digits=10, decimal_places=2)
    eur = models.DecimalField(max_digits=10, decimal_places=2)
    jpy = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Financial Record - {self.create_date}"
