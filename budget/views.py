from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Income,Expense,Budget
from django.db.models import Sum
from .forms import IncomeForm,ExpenseForm,BudgetForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST['Username']
        password = request.POST['pass']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            # Redirect to the dashboard or home page after successful login
            return redirect('Dashboard')  # Replace 'dashboard' with your target page
        else:
            # If authentication fails, show an error message
            return HttpResponse("Invalid login credentials", status=401)

    # If GET request, render the login page
    return render(request, 'login.html')


@login_required
def Dashboard(request):
    
    Expense = calc_totalExpense(request.user)
    Salary = calc_totalIncome(request.user)

    setBudget, remainingBudget = calc_Budget(request.user)

    return render(request,'dashboard.html',{
        'Total_Income': Salary,
        'Total_Expense': Expense,
        'Set_Budget': setBudget,
        'Remaining_Budget': remainingBudget,
    })

from django.contrib import messages


# View to display the sign-up page and handle form submission
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        # Create new user if everything is fine
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully!')
        return redirect('login')  # Redirect to the login page after successful sign-up

    return render(request,'signup.html')  # Render the Sign Up page template




def calc_totalIncome(user):
    # Fetch all income records for the given user
    income_list = Income.objects.filter(user=user)
    
    # Initialize total income
    total_income = 0

    # Iterate through all income records and sum amounts
    for inc in income_list:
        total_income += inc.amount

    return total_income

def calc_totalExpense(user):
    Expense_list = Expense.objects.filter(user = user)

    total_expense = 0

    for exp in Expense_list:
        total_expense += exp.amount

    return total_expense

def calc_Budget(user):
    # Get the budget objects related to the user
    getBudget = Budget.objects.filter(user=user)
    
    # Calculate the total budget by summing the 'amount' from each Budget object
    total_Budget = sum(bud.amount for bud in getBudget)
    
    # Get the total amount of expenses for the user
    spentAmount = calc_totalExpense(user)

    # Calculate the remaining budget
    remainingBudget = total_Budget - spentAmount

    return total_Budget, remainingBudget



# THIS WILL BE FOR MANAGE PAGE
@login_required
def manage(request):
    # Handle adding income, expense, and budget
    if request.method == 'POST':
        # Check which form was submitted (Add Income, Add Expense, Set Budget)
        if 'add_income' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income_form.save()
                messages.success(request, "Income added successfully!")
            else:
                messages.error(request, "Failed to add income.")
        elif 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense_form.save()
                messages.success(request, "Expense added successfully!")
            else:
                messages.error(request, "Failed to add expense.")
        elif 'set_budget' in request.POST:
            budget_form = BudgetForm(request.POST)
            if budget_form.is_valid():
                budget_form.save()
                messages.success(request, "Budget set successfully!")
            else:
                messages.error(request, "Failed to set budget.")

    # Initialize forms
    income_form = IncomeForm()
    expense_form = ExpenseForm()
    budget_form = BudgetForm()

    return render(request, 'manage.html', {
        'income_form': income_form,
        'expense_form': expense_form,
        'budget_form': budget_form
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib import messages

@login_required
def edit_transaction(request, transaction_type, transaction_id):
    """
    Edit an income or expense transaction.
    :param transaction_type: 'income' or 'expense' to indicate which type to edit.
    :param transaction_id: The ID of the transaction to edit.
    """
    if transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id, user=request.user)
        form = IncomeForm(request.POST or None, instance=transaction)
    elif transaction_type == 'expense':
        transaction = get_object_or_404(Expense, id=transaction_id, user=request.user)
        form = ExpenseForm(request.POST or None, instance=transaction)
    else:
        messages.error(request, "Invalid transaction type.")
        return redirect('dashboard')  # or some other redirect if needed
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Transaction updated successfully!')
        return redirect('dashboard')  # Redirect to dashboard or another page
    
    return render(request, 'edit_transaction.html', {'form': form, 'transaction': transaction})




@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Associate with logged-in user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('Dashboard')  # Redirect to dashboard after form submission
    else:
        form = IncomeForm()
    
    return render(request, 'add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate with logged-in user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('Dashboard')  # Redirect to dashboard after form submission
    else:
        form = ExpenseForm()
    
    return render(request, 'add_expense.html', {'form': form})


@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user  # Associate budget with the logged-in user
            budget.save()
            messages.success(request, 'Budget set successfully!')
            return redirect('Dashboard')  # Redirect to dashboard after form submission
    else:
        form = BudgetForm()

    

    return render(request, 'set_budget.html', {'form': form, })



