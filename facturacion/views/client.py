from django.shortcuts import render, redirect
from facturacion.models import Cliente, tipo_documnento

def clientes(request):
    clientes = Cliente.objects.all()
    tipo = tipo_documnento.objects.all()
    context = {
        'segment': 'clientes',
        'clientes': clientes,
        'tipos_documento': tipo
    }
    return render(request, 'Clientes/index.html', context)

def registrar_clientes(request):
    if request.method == 'POST':
        id_tipo_doc = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        nombre = request.POST.get('nombre_apellido')
        
        email = request.POST.get('email')
        telefono = request.POST.get('telefono') 
        direccion = request.POST.get('direccion')
        fecha_registro = request.POST.get('fecha_registro')
        esta_activo = True if request.POST.get('activo') == '1' else False
        
        
        try:
           new_client = Cliente.objects.create(
                tipo_documento_id=id_tipo_doc,
                numero_documento=numero_documento,
                nombre=nombre,
                apellidos="",
                email=email,
                telefono=telefono,
                direccion=direccion,
                fecha_registro=fecha_registro,
                activo=esta_activo
            )
           new_client.save()
           print('Client created successfully!')
           return redirect('/clientes')
        except Exception as e:
            print(f"Error creating client: {e}")
            return redirect('/index')
    else:
        print("Invalid request method!")
        return redirect('/index')