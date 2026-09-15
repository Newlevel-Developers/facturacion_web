from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from facturacion.models import Proveedor
from facturacion.models.ingesroStock import IngresoStock
from facturacion.models.payment import MetodoPago

# ==========================================
# 1. LISTAR PROVEEDORES (READ)
# ==========================================
@login_required
@permission_required('facturacion.view_proveedor', raise_exception=True)
def proveedores(request):
    todos_los_proveedores = Proveedor.objects.all().order_by('-fecha_registro')
    proveedores_activos = todos_los_proveedores.filter(activo=True)
    
    context = {
        'segment': 'proveedores',
        'proveedores': todos_los_proveedores,
        'total_activos': proveedores_activos.count(),
        'total_proveedores': todos_los_proveedores.count(),
    }
    return render(request, 'proveedor/proveedor.html', context)


# ==========================================
# 2. CREAR PROVEEDOR (CREATE)
# ==========================================
@login_required
@permission_required('facturacion.add_proveedor', raise_exception=True)
def crear_proveedor(request):
    if request.method == 'POST':
        rif_cedula = request.POST.get('rif_cedula')
        nombre_razon_social = request.POST.get('nombre_razon_social')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        activo = True if request.POST.get('activo') == 'on' else False

        # Validación básica de duplicados
        if Proveedor.objects.filter(rif_cedula=rif_cedula).exists():
            messages.error(request, f'El RIF/Cédula {rif_cedula} ya se encuentra registrado.')
            return redirect('proveedores')

        try:
            Proveedor.objects.create(
                rif_cedula=rif_cedula,
                nombre_razon_social=nombre_razon_social,
                email=email,
                telefono=telefono,
                direccion=direccion,
                activo=activo
            )
            messages.success(request, f'El proveedor "{nombre_razon_social}" fue registrado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al registrar el proveedor: {e}')

        return redirect('proveedores')
        
    return redirect('proveedores')


# ==========================================
# 3. EDITAR PROVEEDOR (UPDATE)
# ==========================================
@login_required
@permission_required('facturacion.change_proveedor', raise_exception=True)
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        rif_cedula = request.POST.get('rif_cedula')
        nombre_razon_social = request.POST.get('nombre_razon_social')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        activo = 'activo' in request.POST

        # Validar duplicados si se cambió el RIF/Cédula
        if Proveedor.objects.filter(rif_cedula=rif_cedula).exclude(id=id).exists():
            messages.error(request, f'El RIF/Cédula {rif_cedula} ya está asignado a otro proveedor.')
            return redirect('proveedores')

        try:
            proveedor.rif_cedula = rif_cedula
            proveedor.nombre_razon_social = nombre_razon_social
            proveedor.email = email
            proveedor.telefono = telefono
            proveedor.direccion = direccion
            proveedor.activo = activo
            proveedor.save()

            messages.success(request, f'El proveedor "{proveedor.nombre_razon_social}" fue actualizado con éxito.')
        except Exception as e:
            messages.error(request, f'Error al actualizar el proveedor: {e}')

        return redirect('proveedores')

    return redirect('proveedores')


# ==========================================
# 4. ELIMINAR PROVEEDOR (DELETE / DESACTIVAR)
# ==========================================
@login_required
@permission_required('facturacion.delete_proveedor', raise_exception=True)
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        try:
            # Opción A: Eliminación lógica (Recomendada para conservar historial de compras)
            proveedor.activo = False
            proveedor.save()
            messages.success(request, f'El proveedor "{proveedor.nombre_razon_social}" ha sido desactivado.')

            # Opción B: Si prefieres borrarlo completamente de la base de datos, descomenta la siguiente línea:
            # proveedor.delete()
            
        except Exception as e:
            messages.error(request, f'Error al eliminar el proveedor: {e}')

        return redirect('proveedores')

    return redirect('proveedores')



@login_required
def registrar_pago_proveedor(request, ingreso_id):
    ingreso = get_object_or_404(IngresoStock, id=ingreso_id)

    if request.method == 'POST':
        metodo_id = request.POST.get('metodo_pago')
        monto = Decimal(request.POST.get('monto', '0.00'))
        referencia = request.POST.get('referencia', '')
        observaciones = request.POST.get('observaciones', '')

        if monto <= 0:
            messages.error(request, "El monto a pagar debe ser mayor a 0.")
            return redirect('cuentas_por_pagar')

        try:
            with transaction.atomic():
                # 1. Registrar el pago
                metodo = MetodoPago.objects.get(id=metodo_id)
                PagoProveedor.objects.create(
                    ingreso=ingreso,
                    metodo_pago=metodo,
                    monto=monto,
                    referencia=referencia,
                    observaciones=observaciones
                )

                # 2. Verificar total pagado acumulado
                pagos_totales = sum(pago.monto for pago in ingreso.pagos_proveedor.all())

                if pagos_totales >= ingreso.monto_total:
                    ingreso.estado = 'PAGADO'
                    ingreso.save()

                messages.success(request, f"Pago de {monto} registrado exitosamente para la compra #{ingreso.id}.")

        except Exception as e:
            messages.error(request, f"Error al procesar el pago: {str(e)}")

    return redirect('cuentas_por_pagar')


@login_required
def cuentas_por_pagar(request):
    compras_pendientes = IngresoStock.objects.filter(estado='PENDIENTE').order_by('-fecha_ingreso')
    metodos_pago = MetodoPago.objects.filter(activo=True)

    context = {
        'segment': 'cuentas_por_pagar',
        'compras': compras_pendientes,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'proveedor/cuentas_por_pagar.html', context)