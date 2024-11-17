from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum
from .forms import ExpenseForm
from .models import ExpenseAdd

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
    
def expenseView(request):
    return render(request, 'expense-views.html')

def expenseViewApi(request):
    expense_data_perday = ExpenseAdd.objects.values('expense_date').annotate(total_expense = Sum('expense'))
    expenses = []
    for item in expense_data_perday:
        expenses.append({
            'date':item['expense_date'],
            'total_expense' : item['total_expense']
        })
    return JsonResponse({'expenses':expenses})

def homePage(request):
    return render(request, 'home.html')