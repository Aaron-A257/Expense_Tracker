

# Register your models here.

from django.contrib import admin
from .models import UserProfile, Expense, Income,  Budget

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user field in the admin list view

@admin.register(Expense)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'datetime', 'description')  # Customize columns
    search_fields = ('user__username', 'category', 'description')  # Add search functionality
    list_filter = ('category', 'datetime')  # Add filters for better navigation

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount', 'datetime', 'description')
    search_fields = ('user__username', 'source', 'description')
    list_filter = ('datetime',)



@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'period')
    search_fields = ('user__username','category')
    list_filter = ('period', 'category')
