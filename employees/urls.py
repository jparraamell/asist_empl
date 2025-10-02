from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [    
    path('dashboard/', views.dashboard, name='dashboard'),    
    path("register/", views.register_employee, name="register_employee"),  #
    ]