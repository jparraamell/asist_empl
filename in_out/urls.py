from django.urls import path
from . import views

app_name = 'in_out'

urlpatterns = [
    path('input/', views.input_page, name='input'),
    path('output/', views.output_page, name='output'), 
] 