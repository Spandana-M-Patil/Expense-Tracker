from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExpenseAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    expense = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    expense_date = models.DateField()

    def __str__(self) -> str:
        return self.category


