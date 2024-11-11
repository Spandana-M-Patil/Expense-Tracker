from django.db import models
from datetime import date
# Create your models here.
class ExpenseAdd(models.Model):
    expense = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    expense_date = models.DateField()

    def __str__(self) -> str:
        return self.category


