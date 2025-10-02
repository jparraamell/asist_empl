from django.contrib import admin
from .models import Charges, Gender, IdentificationType, Employee

# Register your models here.
admin.site.register(Charges) 
admin.site.register(Gender)
admin.site.register(IdentificationType)
admin.site.register(Employee)