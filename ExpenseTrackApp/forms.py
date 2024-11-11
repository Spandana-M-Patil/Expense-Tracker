from django import forms
from .models import ExpenseAdd

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseAdd
        fields = ['expense', 'category', 'description', 'expense_date']
        widgets = {
            'expense_date' : forms.HiddenInput(),
            'description' : forms.Textarea()
        }
