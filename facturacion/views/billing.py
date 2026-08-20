from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from facturacion.models import Factura, DetalleFactura, Producto, Cliente

def facturas(request):
    todas_las_facturas = Factura.objects.all().order_by('-fecha_emision')
    context = {
        'segment': 'facturas',
        'facturas': todas_las_facturas
    }
    return render(request, 'facturas/facturas_list.html', context)
    
def crear_factura(request):
    if request.method == 'POST':
        # 1. Obtener datos básicos
        cliente_id = request.POST.get('cliente')
        # Para el número de factura, buscamos la última y sumamos 1
        ultima_factura = Factura.objects.last()
        if not ultima_factura:
            nuevo_numero = "F001-000001"
        else:
            # Separa 'F001-000080' por el guion y toma la parte numérica ('000080')
            try:
                numero_actual = int(ultima_factura.numero_factura.split('-')[-1])
            except ValueError:
                # Fallback por si hay facturas viejas que solo tenían números sin la 'F'
                numero_actual = int(ultima_factura.numero_factura)
                
            # Genera el nuevo número manteniendo el formato y sumando 1 (ej. F001-000081)
            nuevo_numero = f"F001-{numero_actual + 1:06d}"
        
        # 2. Obtener listas de productos (desde el frontend)
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        
        try:
            # Usamos una transacción para que si algo falla, no se guarde nada
            with transaction.atomic():
                # Creamos la cabecera de la factura primero con valores en 0
                nueva_factura = Factura.objects.create(
                    numero_factura=str(nuevo_numero).zfill(8), # Ej: 00000001
                    tipo_comprobante="FACTURA",
                    fecha_emision=timezone.now(),
                    subtotal=0,
                    igv=0,
                    total=0,
                    estado="PAGADO",
                    cliente_id=cliente_id,
                    usuario=request.user
                )

                total_subtotal = Decimal('0.00')
                tasa_iva = Decimal('0.16') # 16% IVA Venezuela

                for p_id, cant in zip(productos_ids, cantidades):
                    producto = Producto.objects.get(id=p_id)
                    cantidad = int(cant)
                    
                    if producto.stock < cantidad:
                        raise Exception(f"Stock insuficiente para {producto.nombre}")
                    p_subtotal = producto.precio_venta * cantidad
                    
                    # Crear el detalle
                    DetalleFactura.objects.create(
                        factura=nueva_factura,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio_venta,
                        subtotal=p_subtotal
                    )

                    # Descontar Stock
                    producto.stock -= cantidad
                    producto.save()

                    total_subtotal += p_subtotal

                # 3. Cálculos Finales de la Factura
                impuesto = total_subtotal * tasa_iva
                total_final = total_subtotal + impuesto

                # Actualizamos la cabecera con los totales reales
                nueva_factura.subtotal = total_subtotal
                nueva_factura.igv = impuesto
                nueva_factura.total = total_final
                nueva_factura.save()

            return redirect('/billing') # O a la vista de impresión

        except Exception as e:
            print(f"Error en facturación: {e}")
            return redirect('/billing')
            
    return redirect('/billing')

def billing(request):
    hoy = timezone.localdate()
    todas_las_facturas = Factura.objects.all()
    facturas = Factura.objects.filter(fecha_emision__date=hoy).order_by('-fecha_emision')[:5]
    # Obtenemos los clientes para la sección "Billing Information"
    clientes_billing = Cliente.objects.filter(activo=True)[:3]
    
    # Calculamos algunos totales para las tarjetas superiores (opcional)
    total_ingresos = sum(f.total for f in Factura.objects.filter(estado='Pagado'))
    status_paid = todas_las_facturas.filter(estado = 'PAGADO')
    status_paids = status_paid.count()
    context = {
        'facturas': facturas,
        'clientes': clientes_billing,
        'total_ingresos': total_ingresos,
        'todas_las_facturas': todas_las_facturas,
        'status_paids': status_paids
        
    }
    return render(request, 'facturas/billing.html', context)

def detalle_factura(request, factura_id):
    # Buscamos la factura o devolvemos 404 si no existe
    factura = get_object_or_404(Factura, id=factura_id)
    # Filtramos los productos que se vendieron en esa factura específica
    detalles = DetalleFactura.objects.filter(factura=factura)
    
    context = {
        'segment': 'facturas',
        'factura': factura,
        'detalles': detalles
    }
    return render(request, 'facturas/detalle_factura.html', context)