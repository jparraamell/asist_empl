from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuarios de Django


# Create your models here.
class Charges(models.Model):
    id_charge = models.AutoField(primary_key=True)
    charge_name = models.CharField(
        max_length=100, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Charge name (e.g., Manager, Developer)"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Charge creation date and time"
    )
    
    def __str__(self):
        """String representation of Charge object"""
        return self.charge_name

    class Meta:
        db_table = 'charges'
        verbose_name = 'Charge'
        verbose_name_plural = 'Charges'
        ordering = ['charge_name']
        
class Gender(models.Model):
    id_gender = models.AutoField(primary_key=True)
    gender_name = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False,
        help_text="Gender name (e.g., Male, Female)"
    )

    def __str__(self):
        """String representation of Gender object"""
        return self.gender_name

    class Meta:
        db_table = 'genders'
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'
        ordering = ['gender_name']

class IdentificationType(models.Model):
    id_identification_type = models.AutoField(primary_key=True)
    type_name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        help_text="Type of identification (e.g., Passport, Driver's License)"
    )

    def __str__(self):
        """String representation of IdentificationType object"""
        return self.type_name

    class Meta:
        db_table = 'identification_types'
        verbose_name = 'Identification Type'
        verbose_name_plural = 'Identification Types'
        ordering = ['type_name']

class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    qr_code = models.BigIntegerField(   # para códigos QR largos numéricos
        unique=True,
        null=False,
        blank=False,
        help_text="Unique numeric QR code for the employee"
    )
    first_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        help_text="Employee's first name"
    )
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        help_text="Employee's last name"
    )
    second_last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Employee's second last name (if applicable)"
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.PROTECT,
        related_name='employees',
    )
    direction = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Employee's address"
    )
    identification_type = models.ForeignKey(
        IdentificationType,
        on_delete=models.PROTECT,
        related_name='employees',
        help_text="Type of identification"
    )
    identification_number = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        help_text="Unique identification number"
    )
    number_phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="Employee's phone number"
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        help_text="Employee's email address"
    )
    date_birthday = models.DateField(
        null=False,
        blank=False,
        help_text="Employee's date of birth"
    )
    charge = models.ForeignKey(
        Charges,
        on_delete=models.PROTECT,
        related_name='employees',
        help_text="Employee's job position"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="employees_created",
        help_text="User who created this employee record"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['last_name', 'first_name']
