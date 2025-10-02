from django.db import models

# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol_name = models.CharField(
        max_length=50, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Role name (e.g., Administrator, User)"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Role creation date and time"
    )
    
    def __str__(self):
        """String representation of Role object"""
        return self.rol_name

    class Meta:
        db_table = 'rol'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['rol_name']

#User class
class User(models.Model):
    id_user = models.BigAutoField(
        primary_key=True,
        help_text="Unique user ID"
    )
    username = models.CharField(
        max_length=150, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Unique username (3-20 alphanumeric characters)"
    )
    email = models.EmailField(
        max_length=255, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="User's unique email address"
    )
    password = models.CharField(
        max_length=255, 
        null=False, 
        blank=False,
        help_text="User's hashed password"
    )
    user_state = models.BooleanField(
        default=True, 
        null=False,
        help_text="User state (True=Active, False=Inactive)"
    )
    rol = models.ForeignKey(
        'Rol', 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False,
        help_text="Role assigned to user"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="User registration date and time"
    )
    
    
    def is_active(self):
        """
        Check if user is active.
        
        Returns:
            bool: True if user_state is True, False otherwise
        """
        return self.user_state
    
    def get_role_name(self):
        """
        Get user's role name.
        
        Returns:
            str: Name of the role assigned to user
        """
        return self.rol.rol_name if self.rol else "No role"
    
    def __str__(self):
        """
        String representation of User object.
        
        Returns:
            str: User's username
        """
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']  # Most recent users first
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['user_state']),
        ]