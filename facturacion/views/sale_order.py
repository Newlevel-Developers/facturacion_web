from django.shortcuts import render, redirect
from facturacion.models import Producto, tipo_documnento,Cliente
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('facturacion.sele_order', raise_exception=True)
def nueva_venta(request):
    productos_disponibles = Producto.objects.filter(activo=True, stock__gt=0)
    clientes = Cliente.objects.all()
    tipo = tipo_documnento.objects.all()
    context = {
        'segment': 'nueva_venta',
        'productos': productos_disponibles,
        'clientes': clientes,
        'tipos_documento': tipo
    }
    return render(request, 'pages/ventas.html', context)

@permission_required('facturacion.sele_order', raise_exception=True)
def registrar_compra(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad_comprada = int(request.POST.get('cantidad'))
        costo_unitario = Decimal(request.POST.get('precio_compra'))

        try:
            with transaction.atomic():
                producto = Producto.objects.get(id=producto_id)
                
                # Actualizamos el stock (Trazabilidad de entrada)
                producto.stock += cantidad_comprada
                
                # Opcional: Actualizamos el precio de compra si cambió
                producto.precio_compra = costo_unitario
                producto.save()
                
                # Aquí podrías crear un modelo 'IngresoStock' para historial detallado
                print(f"Entrada de stock: {producto.nombre} +{cantidad_comprada}")
                
            return redirect('/productos')
        except Exception as e:
            print(f"Error en compra: {e}")
            return redirect('/index')
