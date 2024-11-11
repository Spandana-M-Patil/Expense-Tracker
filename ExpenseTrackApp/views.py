from django.shortcuts import render, redirect
from .forms import ExpenseForm
from django.http import HttpResponse
from datetime import date

# Create your views here.
def expenseAddView(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print("Form errors:", form.errors)  # Shows any validation issues
    else:
        form = ExpenseForm()

    return render(request, 'dashboard.html', {'form': form})
