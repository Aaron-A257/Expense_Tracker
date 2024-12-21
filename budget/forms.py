# budget/forms.py
from django import forms
from .models import Income,Expense,Budget

class IncomeForm(forms.ModelForm):
    # Example form fields, replace with your actual form fields
    class Meta:
        model = Income
        fields = ['source','amount','datetime','description']
    # Add any other fields you need


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'datetime', 'description']

class BudgetForm(forms.ModelForm):
    
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period']