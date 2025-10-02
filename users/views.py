from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import User, Rol
from django.db.models import Q
from django.contrib.auth.models import User as DjangoUser


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('username', '').strip()  # puede ser username o email
        password = request.POST.get('password', '')

        try:
            # Buscar usuario por username o email
            user = User.objects.get(Q(username=login_input) | Q(email=login_input), password=password)
            
            # Guardar info en sesión
            request.session['user_id'] = user.id_user
            request.session['username'] = user.username
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('employees:dashboard')
        except User.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rol_id = request.POST.get('rol', 1)  # default rol_id = 1
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios') 
            return render(request, 'register.html')
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'register.html')
        try:
            rol_instance = Rol.objects.get(id_rol=rol_id)
            
            user = User.objects.create(
                username=username,
                email=email,
                password=password1,
                rol=rol_instance
            )
            messages.success(request, f'¡Cuenta creada exitosamente para {username}!')
            return redirect('users:login')
        except Rol.DoesNotExist:
            messages.error(request, 'El rol seleccionado no existe')
        except IntegrityError:
            messages.error(request, 'Este nombre de usuario o email ya existe')
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
    return render(request, 'register.html')