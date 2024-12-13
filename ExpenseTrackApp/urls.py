"""
URL configuration for ExpenseTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ExpenseTrackApp import views

urlpatterns = [
    path('home/', views.homePage),
    path('views/', views.expenseView),
    path('add/', views.expenseAddView),
    path('api-expenseView/', views.expenseViewApi),
    path('day-details/<str:date>/', views.day_details, name='day-details'),
    path('fetch-expense-data/<int:id>/', views.fetch_expense_data),
    path('expenses/', views.view_expense, name='view_expense'),
    path('fetchViewExpense/<str:start>/<str:end>/<str:selectCategory>/', views.fetchTheExpenses, name='fetchTheExpenses'),
    path('categoryList/', views.category_list, name='category_list'),
    path('', views.register_page, name='register_page'),
    path('login/', views.login_page, name="login"),
    path('documentation/', views.documentation_page, name='documentation')

]
