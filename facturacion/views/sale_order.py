from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from decimal import Decimal

from facturacion.models import Producto, TipoDocumento, Cliente, Factura, DetalleFactura

@login_required
@permission_required('facturacion.sele_order', raise_exception=True)
def nueva_venta(request):
    if request.method == 'POST':
        # 1. Captura de datos del cliente y forma de pago
        cliente_id = request.POST.get('cliente')
        metodo_pago = request.POST.get('metodo_pago')
        observaciones_credito = request.POST.get('observaciones_credito', '')
        
        # Listas de productos recibidas de la tabla dinámica
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')

        # Montos opcionales enviables desde el formulario
        descuento_post = Decimal(request.POST.get('descuento', '0.00') or '0.00')

        if not cliente_id or not productos_ids:
            messages.error(request, "Debe seleccionar un cliente y al menos un producto.")
            return redirect('nueva_venta')

        try:
            with transaction.atomic():
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Instanciamos la factura previa a calcular totales
                factura = Factura.objects.create(
                    cliente=cliente,
                    metodo_pago=metodo_pago,
                    observaciones=observaciones_credito,
                    usuario=request.user,
                    subtotal=Decimal('0.00'),
                    iva=Decimal('0.00'),
                    descuento=descuento_post,
                    total=Decimal('0.00')
                )

                subtotal_acumulado = Decimal('0.00')

                # 2. Recorrer productos y procesar stock + líneas de factura
                for prod_id, cant in zip(productos_ids, cantidades):
                    if not prod_id:
                        continue

                    producto = Producto.objects.select_for_update().get(id=prod_id)
                    cantidad_vendida = int(cant)
                    
                    if producto.stock < cantidad_vendida:
                        raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}. Disponible: {producto.stock}")

                    # Descuento de stock
                    producto.stock -= cantidad_vendida
                    producto.save()

                    # Precio unitario obtenido del modelo (evita manipulación en frontend)
                    precio_unitario = producto.precio_venta
                    subtotal_linea = precio_unitario * cantidad_vendida

                    # Registrar detalle
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad_vendida,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal_linea
                    )

                    subtotal_acumulado += subtotal_linea

                # 3. Cálculo fiscal (IVA 16% + Descuentos)
                iva_calculado = subtotal_acumulado * Decimal('0.16')
                total_con_iva = subtotal_acumulado + iva_calculado
                total_final = max(total_con_iva - descuento_post, Decimal('0.00'))

                # Actualizamos cabecera de la factura
                factura.subtotal = subtotal_acumulado
                factura.iva = iva_calculado
                factura.total = total_final
                factura.save()

                messages.success(request, f"Factura #{factura.id} registrada exitosamente.")
                return redirect('/facturas')

        except Producto.DoesNotExist:
            messages.error(request, "Uno de los productos seleccionados no existe.")
            return redirect('nueva_venta')
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente seleccionado no existe.")
            return redirect('nueva_venta')
        except Exception as e:
            messages.error(request, f"Error al procesar la venta: {str(e)}")
            return redirect('nueva_venta')

    # Método GET: Muestra la interfaz gráfica
    productos_disponibles = Producto.objects.filter(activo=True, stock__gt=0)
    clientes = Cliente.objects.all()
    tipo = TipoDocumento.objects.all()
    
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
        cantidad_comprada = int(request.POST.get('cantidad', 0))
        costo_unitario = Decimal(request.POST.get('precio_compra', '0.00'))

        try:
            with transaction.atomic():
                producto = Producto.objects.select_for_update().get(id=producto_id)
                
                # Actualizamos el stock (Trazabilidad de entrada)
                producto.stock += cantidad_comprada
                
                # Actualizamos el precio de compra
                producto.precio_compra = costo_unitario
                producto.save()
                
                messages.success(request, f"Stock actualizado para {producto.nombre} (+{cantidad_comprada}).")
                
            return redirect('/productos')
        except Exception as e:
            messages.error(request, f"Error en compra: {str(e)}")
            return redirect('/index')