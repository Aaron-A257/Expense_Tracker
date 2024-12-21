from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=70)
    amount = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    datetime = models.DateTimeField("Date of Expense")
    description = models.CharField(max_length=200)
    
    
    def __str__(self):
        return f"{self.source} - {self.amount}"



class Income(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    source = models.CharField(max_length=200)
    datetime = models.DateTimeField("Date of Expense")
    description = models.CharField(max_length=200)

     

class Budget(models.Model):
    types = [
        ('income' , 'Income'),
        ('expense' , 'Expense')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=7, choices=types)
    amount = models.DecimalField(default=0,max_digits=8,decimal_places=2)

    budget_types = [
        ('Weekly','weekly'),
        ('Monthly','monthly'),
        ('Yearly','yearly')
    ]
    

    period = models.CharField(max_length=7,choices=budget_types)

   
