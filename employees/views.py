from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Employee, Charges, Gender, IdentificationType
import qrcode
import io
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from reportlab.lib.utils import ImageReader

def dashboard(request):
    """Dashboard que incluye todos los datos necesarios para los modales"""
    total_employees = Employee.objects.count()
    charges = Charges.objects.all()
    genders = Gender.objects.all()
    identification_types = IdentificationType.objects.all()
    
    context = {
        'total_employees': total_employees,
        'charges': charges,
        'genders': genders,
        'identification_types': identification_types,
    }
    
    return render(request, 'dashboard.html', context)

def register_employee(request):
    """Registrar empleado - Sin @login_required"""
    # Verificar si el usuario está logueado con nuestro sistema personalizado
    if 'user_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para registrar empleados')
        return redirect('users:login')
    
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            charge = get_object_or_404(Charges, pk=request.POST.get("charge"))
            gender = get_object_or_404(Gender, pk=request.POST.get("gender"))
            identification_type = get_object_or_404(IdentificationType, pk=request.POST.get("type_identification"))
            
            # Generar QR code único
            qr_code = random.randint(100000000, 999999999)
            while Employee.objects.filter(qr_code=qr_code).exists():
                qr_code = random.randint(100000000, 999999999)
            
            # Crear empleado con los nombres de campos correctos del modelo
            employee = Employee.objects.create(
                qr_code=qr_code,
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                second_last_name="",  # Campo opcional
                gender=gender,
                direction=request.POST.get("address"),  # Mapear address a direction
                identification_type=identification_type,
                identification_number=request.POST.get("position"),  # Mapear position a identification_number
                number_phone=request.POST.get("phone"),  # Mapear phone a number_phone
                email=request.POST.get("email"),
                date_birthday=request.POST.get("birthday"),  # Mapear birthday a date_birthday
                charge=charge,
                created_by_id=request.session['user_id']  # Usar user_id de la sesión
            )

            # Generar el QR
            qr_img = qrcode.make(str(employee.qr_code))

            # Crear PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.setFont("Helvetica-Bold", 16)
            
            # Título
            p.drawString(100, 800, "TARJETA DE EMPLEADO")
            
            # Información
            p.setFont("Helvetica", 12)
            p.drawString(100, 760, f"Empleado: {employee.first_name} {employee.last_name}")
            p.drawString(100, 740, f"Código: {employee.qr_code}")
            p.drawString(100, 720, f"Cargo: {charge.charge_name}")
            p.drawString(100, 700, f"Email: {employee.email}")
            p.drawString(100, 680, f"Identificación: {employee.identification_number}")

            # QR en PDF
            qr_bytes = io.BytesIO()
            qr_img.save(qr_bytes, format="PNG")
            qr_bytes.seek(0)
            qr_image = ImageReader(qr_bytes)
            p.drawImage(qr_image, 100, 500, width=150, height=150)

            # Instrucciones
            p.setFont("Helvetica", 10)
            p.drawString(100, 450, "Escanea este código QR para registrar tu asistencia")

            p.showPage()
            p.save()
            buffer.seek(0)
            
            messages.success(request, f'Empleado {employee.first_name} {employee.last_name} registrado exitosamente')
            
            return FileResponse(
                buffer, 
                as_attachment=True, 
                filename=f"Empleado_{employee.qr_code}_QR.pdf"
            )
            
        except Exception as e:
            messages.error(request, f'Error al registrar empleado: {str(e)}')
            print(f"Error detallado: {e}")  # Para debug
            return redirect('employees:dashboard')

    # Si es GET, redirigir al dashboard
    return redirect(request,'employees:dashboard')