from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .forms import ExpenseForm
from .models import ExpenseAdd
from django.urls import reverse_lazy
import json
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.
def expenseAddView(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add')
        else:
            print("Form errors:", form.errors)  # Shows any validation issues
    else:
        form = ExpenseForm()

    return render(request, 'dashboard.html', {'form': form}) 
    
def expenseView(request):
    return render(request, 'expense-views.html')

# API end point
def expenseViewApi(request):
    expense_data_perday = ExpenseAdd.objects.values('expense_date').annotate(total_expense = Sum('expense'))
    
    expenses = []
    for item in expense_data_perday:
        daily_expenses = ExpenseAdd.objects.filter(expense_date = item['expense_date']).values('description','category', 'id')
        expenses.append({
            'date':item['expense_date'],
            'total_expense' : item['total_expense'],
            'details' : list(daily_expenses)
        })
    return JsonResponse({'expenses':expenses})

def homePage(request):
    return render(request, 'home.html')

@never_cache
def day_details(request, date):
    # Fetch expenses for the selected date
    expenses = ExpenseAdd.objects.filter(expense_date=date)
    
    if request.method == 'POST':
        # Handle delete action
        if 'delete' in request.POST:
            expense_id = request.POST.get('expense_id')
            expense = get_object_or_404(ExpenseAdd, id=expense_id)
            expense.delete()
            messages.success(request, 'Expense delted successfully!!')
            return redirect(reverse_lazy('day-details', args=[date]))
        
        # Handle edit action
        elif 'edit' in request.POST:
            expense_id = request.POST.get('expense_id')
            expense = get_object_or_404(ExpenseAdd, id=expense_id)
            form = ExpenseForm(request.POST, instance=expense)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('day-details', args=[date]))
        else:
            # Pass the form with errors to the template
            return render(request, 'day_details.html', {
                'expenses': expenses,
                'form': form,
                'selected_date': date,
            })

    else:
        # Initialize an empty form for adding new expenses (if applicable)
        form = ExpenseForm()

    # Render the template with expenses and form
    return render(request, 'day_details.html', {
        'expenses': expenses,
        'form': form,
        'selected_date': date,
    })


def fetch_expense_data(request, id):
    if request.method == 'GET':
        expenses = get_object_or_404(ExpenseAdd, id=id)
        data = {
            'id': expenses.id,
            'date':expenses.expense_date,
            'category': expenses.category,
            'amount': expenses.expense,
            'description': expenses.description,
        }
        return JsonResponse(data)
