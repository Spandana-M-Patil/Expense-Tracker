from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .forms import ExpenseForm
from .models import ExpenseAdd
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def expenseAddView(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate with the logged-in user
            expense.save()
            return redirect('/add')
        else:
            print("Form errors:", form.errors)  # Debugging purpose
    else:
        form = ExpenseForm()

    return render(request, 'dashboard.html', {'form': form}) 

@login_required
def expenseView(request):
    return render(request, 'expense-views.html')

# API endpoint
@login_required
def expenseViewApi(request):
    expense_data_perday = ExpenseAdd.objects.filter(user=request.user).values('expense_date').annotate(total_expense=Sum('expense'))
    expenses = []
    for item in expense_data_perday:
        daily_expenses = ExpenseAdd.objects.filter(user=request.user, expense_date=item['expense_date']).values('description', 'category', 'id')
        expenses.append({
            'date': item['expense_date'],
            'total_expense': item['total_expense'],
            'details': list(daily_expenses)
        })
    return JsonResponse({'expenses': expenses})

@login_required
def homePage(request):
    return render(request, 'home.html')

@never_cache
@login_required
def day_details(request, date):
    # Fetch expenses for the selected date
    expenses = ExpenseAdd.objects.filter(user=request.user, expense_date=date)
    
    if request.method == 'POST':
        # Handle delete action
        if 'delete' in request.POST:
            expense_id = request.POST.get('expense_id')
            expense = get_object_or_404(ExpenseAdd, id=expense_id, user=request.user)  # Ensure user owns the expense
            expense.delete()
            messages.success(request, 'Expense deleted successfully!')
            return redirect(reverse_lazy('day-details', args=[date]))
        
        # Handle edit action
        elif 'edit' in request.POST:
            expense_id = request.POST.get('expense_id')
            expense = get_object_or_404(ExpenseAdd, id=expense_id, user=request.user)  # Ensure user owns the expense
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

@login_required
def fetch_expense_data(request, id):
    if request.method == 'GET':
        expense = get_object_or_404(ExpenseAdd, id=id, user=request.user)  # Ensure user owns the expense
        data = {
            'id': expense.id,
            'date': expense.expense_date,
            'category': expense.category,
            'amount': expense.expense,
            'description': expense.description,
        }
        return JsonResponse(data)

@login_required
def view_expense(request):
    return render(request, "viewexpense.html")

@login_required
def fetchTheExpenses(request, start, end, selectCategory):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    selectCategory = selectCategory.lower()
    expenses = ExpenseAdd.objects.filter(user=request.user, expense_date__gte=start_date, expense_date__lte=end_date, category=selectCategory)
    expense_list = list(expenses.values())
    sum_range = expenses.aggregate(total_sum=Sum('expense'))

    return JsonResponse({'expenses': expense_list, 'total': sum_range})

@login_required
def category_list(request):
    category_list = list(ExpenseAdd.objects.filter(user=request.user).values('category').distinct())
    return JsonResponse({'category': category_list})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    return render(request, 'register.html')

def documentation_page(request):
    return render(request, 'documentation.html')