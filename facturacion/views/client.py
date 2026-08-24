from django.shortcuts import render, redirect,get_object_or_404
from facturacion.models import Cliente, tipo_documnento
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('facturacion.view_cliente', raise_exception=True)
def clientes(request):
    clientes = Cliente.objects.all()
    clientes_activos = clientes.filter(activo=True)
    if clientes.exists():
        ultimo_registro = clientes.latest('fecha_registro')
    else:
        ultimo_registro = None
    tipo = tipo_documnento.objects.all()
    context = {
        'segment': 'clientes',
        'clientes': clientes,
        'clientes_activos': clientes_activos,
        'ultimo_registro': ultimo_registro,
        'tipos_documento': tipo
    }
    return render(request, 'Clientes/index.html', context)

@login_required
@permission_required('facturacion.add_cliente', raise_exception=True)
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
    
@login_required
@permission_required('facturacion.change_cliente', raise_exception=True)
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        id_tipo_doc = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        nombre = request.POST.get('nombre_apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        # CORRECCIÓN: Evaluar '1' como True y '0' como False
        activo = True if request.POST.get('activo') == '1' else False

        if not all([id_tipo_doc, numero_documento, nombre]):
            messages.error(request, "El tipo de documento, número y nombre son obligatorios.")
            return redirect('clientes')

        try:
            cliente.tipo_documento_id = id_tipo_doc
            cliente.numero_documento = numero_documento
            cliente.nombre = nombre
            cliente.email = email
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.activo = activo
            
            cliente.save()

            messages.success(request, f'¡El cliente "{cliente.nombre}" se actualizó correctamente!')
            return redirect('clientes')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar el cliente: {e}")
            return redirect('clientes')

    return redirect('clientes')

@login_required
@permission_required('facturacion.delete_cliente', raise_exception=True)
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    try:
        cliente.activo = False
        cliente.save()
        messages.success(request, f'El cliente "{cliente.nombre}" fue desactivado con éxito.')
        # cliente.delete()
        # messages.success(request, f'El cliente "{cliente.nombre}" fue eliminado permanentemente.')

    except Exception as e:
        messages.error(request, f'Error al eliminar el cliente: {e}')

    return redirect('clientes')