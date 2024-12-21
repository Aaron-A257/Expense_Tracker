from django.urls import path
from . import views

urlpatterns =[
    path('',views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('Dashboard/',views.Dashboard, name ='Dashboard'),
    path('Dashboard/manage/',views.manage, name='manage'),
    path('Dashboard/manage/add_income/', views.add_income, name='add_income'),
    path('Dashboard/manage/add_expense/', views.add_expense, name='add_expense'),
    path('Dashboard/manage/set_budget/', views.set_budget, name='set_budget'),
]