from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, Q
import datetime
from .models import Expense, Category, Budget
from .forms import ExpenseForm, CategoryForm, BudgetForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    today = datetime.date.today()
    current_month_expenses = Expense.objects.filter(user=request.user, date__month=today.month, date__year=today.year)
    total_spent = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate previous month
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 1
    else:
        prev_month = today.month - 1
        prev_year = today.year
        
    prev_month_expenses = Expense.objects.filter(user=request.user, date__month=prev_month, date__year=prev_year)
    prev_total = prev_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Highest spending category
    category_summary = current_month_expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    highest_category = category_summary[0] if category_summary else None
    
    # Check overall budget
    first_day = today.replace(day=1)
    budget = Budget.objects.filter(user=request.user, category__isnull=True, month=first_day).first()
    alert = False
    amount_left = None
    if budget:
        if total_spent > budget.amount:
            alert = True
        amount_left = float(budget.amount) - float(total_spent)
        if amount_left < 0: amount_left = 0

    context = {
        'total_spent': float(total_spent),
        'prev_total': float(prev_total),
        'highest_category': highest_category,
        'recent_expenses': current_month_expenses.order_by('-date', '-created_at')[:5],
        'alert': alert,
        'budget': budget,
        'amount_left': amount_left,
        'chart_labels': [c['category__name'] for c in category_summary][:5],
        'chart_data': [float(c['total']) for c in category_summary][:5],
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def expense_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    expenses = Expense.objects.filter(user=request.user)
    if query:
        expenses = expenses.filter(description__icontains=query)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
        
    categories = Category.objects.filter(Q(user=request.user) | Q(is_predefined=True))
    
    return render(request, 'tracker/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'tracker/expense_form.html', {'form': form, 'is_edit': True})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/expense_confirm_delete.html', {'expense': expense})

@login_required
def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    
    user_categories = Category.objects.filter(user=request.user)
    return render(request, 'tracker/categories.html', {'form': form, 'user_categories': user_categories})

@login_required
def budgets(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            
            # Normalize month to first day of month
            budget.month = budget.month.replace(day=1)
            
            # Handle unique constraints or update existing instead of crash
            existing = Budget.objects.filter(user=request.user, category=budget.category, month=budget.month).first()
            if existing:
                existing.amount = budget.amount
                existing.save()
            else:
                budget.save()
                
            return redirect('budgets')
    else:
        # Pre-fill month for convenience
        form = BudgetForm(user=request.user, initial={'month': datetime.date.today().replace(day=1)})
        
    user_budgets = Budget.objects.filter(user=request.user).order_by('-month', 'category')
    return render(request, 'tracker/budgets.html', {'form': form, 'user_budgets': user_budgets})
