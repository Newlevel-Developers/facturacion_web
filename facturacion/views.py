from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import *
from .models import *
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from django.shortcuts import redirect
from .models import Producto, Categoria


# def login(request):
#   if request.method == 'POST':
#     form = LoginForm(request, data=request.POST)
#     if form.is_valid():
#       user = form.get_user()
#       auth_login(request, user)
#       print('Login successful!')
#       return redirect('/index')
#     else:
#       print("Login failed!")
#   else:
#     form = LoginForm()
  
#   context = {'form': form}
#   return render(request, 'pages/sign-in.html', context)

# def index(request):
#     context = {
#         'segment': 'dashboard'
#     }
#     return render(request, 'pages/index.html', context)

# def productos(request):
    
#     productos = Producto.objects.all()   
#     categorias = Categoria.objects.all()       
#     context = {
#         'segment': 'productos',
#         'productos': productos,
#         'categorias': categorias
#     }
#     return render(request, 'Productos/index.html', context)

# def crear_producto(request):
#     if request.method == 'POST':
#         # 1. Captura de todos los campos del formulario
#         codigo = request.POST.get('codigo')
#         nombre = request.POST.get('nombre')
#         descripcion = request.POST.get('descripcion')
#         precio_compra = request.POST.get('precio_compra')
#         precio_venta = request.POST.get('precio_venta')
#         stock = request.POST.get('stock')
#         stock_minimo = request.POST.get('stock_minimo')
#         categoria_id = request.POST.get('categoria')
        
#         # Manejo del checkbox (booleanos en Django)
#         activo = True if request.POST.get('activo') == 'on' else False
        
#         # 2. Captura de la imagen (requiere request.FILES)
#         imagen = request.FILES.get('imagen')

#         try:
#             # 3. Creación con los nombres exactos de tu modelo/base de datos
#             new_producto = Producto.objects.create(
#                 codigo=codigo,                     # Faltaba
#                 nombre=nombre,
#                 descripcion=descripcion,
#                 precio_compra=precio_compra,       # Tu SQL usa precio_compra
#                 precio_venta=precio_venta,         # Tu SQL usa precio_venta
#                 stock=stock,                       # Faltaba
#                 stock_minimo=stock_minimo,         # Faltaba
#                 imagen=imagen,                     # Faltaba manejar el archivo
#                 activo=activo,                     # Faltaba
#                 categoria_id=categoria_id
#             )
            
#             return redirect('/productos')
            
#         except Exception as e:
#             print(f"Error al crear producto: {e}")
#             return redirect('/index')
#     else:
#         return redirect('/index')

# def clientes(request):
#     clientes = Cliente.objects.all()
#     tipo = tipo_documnento.objects.all()
#     context = {
#         'segment': 'clientes',
#         'clientes': clientes,
#         'tipos_documento': tipo
#     }
#     return render(request, 'Clientes/index.html', context)

# def registrar_clientes(request):
#     if request.method == 'POST':
#         id_tipo_doc = request.POST.get('tipo_documento')
#         numero_documento = request.POST.get('numero_documento')
#         nombre = request.POST.get('nombre_apellido')
        
#         email = request.POST.get('email')
#         telefono = request.POST.get('telefono') 
#         direccion = request.POST.get('direccion')
#         fecha_registro = request.POST.get('fecha_registro')
#         esta_activo = True if request.POST.get('activo') == '1' else False
        
        
#         try:
#            new_client = Cliente.objects.create(
#                 tipo_documento_id=id_tipo_doc,
#                 numero_documento=numero_documento,
#                 nombre=nombre,
#                 apellidos="",
#                 email=email,
#                 telefono=telefono,
#                 direccion=direccion,
#                 fecha_registro=fecha_registro,
#                 activo=esta_activo
#             )
#            new_client.save()
#            print('Client created successfully!')
#            return redirect('/clientes')
#         except Exception as e:
#             print(f"Error creating client: {e}")
#             return redirect('/index')
#     else:
#         print("Invalid request method!")
#         return redirect('/index')

# def charts(request):
#     context = {
#         'segment': 'charts'
#     }
#     return render(request, 'charts/index.html', context)

# def usuarios(request):
#     usuarios = User.objects.all()
#     context = {
#         'segment': 'usuarios',
#         'usuarios': usuarios
#     }
#     return render(request, 'pages/usuarios.html', context)

# def registrar_usuario(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if not username or not email or not password or not first_name or not last_name:
#             print("All fields are required!")
#             return redirect('/index')
#         try:
#             new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
#             new_user.save()
#             print('User created successfully!')
#             return redirect('/tables')
#         except Exception as e:
#             print(f"Error creating user: {e}")
#             return redirect('/index')
#     else:
#         print("Invalid request method!")
#         return redirect('/index')

# def editar_usuario(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
        
#         try:
#             user = User.objects.get(id=user_id)
#             user.first_name = request.POST.get('first_name')
#             user.last_name = request.POST.get('last_name')
#             user.email = request.POST.get('email')
#             user.username = request.POST.get('username')
            
#             # Validación simple
#             if not all([user.first_name, user.last_name, user.email, user.username]):
#                 messages.error(request, "Todos los campos son obligatorios.")
#                 return redirect('/tables')

#             user.save()
#             messages.success(request, '¡Usuario actualizado correctamente!')
#             return redirect('/tables')
            
#         except User.DoesNotExist:
#             messages.error(request, "Usuario no encontrado.")
#         except Exception as e:
#             messages.error(request, f"Error: {e}")
        
#         return redirect('/tables')
    
#     return redirect('/index')

# def facturas(request):
#     todas_las_facturas = Factura.objects.all().order_by('-fecha_emision')
#     context = {
#         'segment': 'facturas',
#         'facturas': todas_las_facturas
#     }
#     return render(request, 'facturas/facturas_list.html', context)
    
# def crear_factura(request):
#     if request.method == 'POST':
#         # 1. Obtener datos básicos
#         cliente_id = request.POST.get('cliente')
#         # Para el número de factura, buscamos la última y sumamos 1
#         ultima_factura = Factura.objects.last()
#         nuevo_numero = 1 if not ultima_factura else int(ultima_factura.numero_factura) + 1
        
#         # 2. Obtener listas de productos (desde el frontend)
#         productos_ids = request.POST.getlist('producto_id[]')
#         cantidades = request.POST.getlist('cantidad[]')
        
#         try:
#             # Usamos una transacción para que si algo falla, no se guarde nada
#             with transaction.atomic():
#                 # Creamos la cabecera de la factura primero con valores en 0
#                 nueva_factura = Factura.objects.create(
#                     numero_factura=str(nuevo_numero).zfill(8), # Ej: 00000001
#                     tipo_comprobante="FACTURA",
#                     fecha_emision=timezone.now(),
#                     subtotal=0,
#                     igv=0,
#                     total=0,
#                     estado="PAGADO",
#                     cliente_id=cliente_id,
#                     usuario=request.user
#                 )

#                 total_subtotal = Decimal('0.00')
#                 tasa_iva = Decimal('0.16') # 16% IVA Venezuela

#                 for p_id, cant in zip(productos_ids, cantidades):
#                     producto = Producto.objects.get(id=p_id)
#                     cantidad = int(cant)
                    
#                     if producto.stock < cantidad:
#                         raise Exception(f"Stock insuficiente para {producto.nombre}")
#                     p_subtotal = producto.precio_venta * cantidad
                    
#                     # Crear el detalle
#                     DetalleFactura.objects.create(
#                         factura=nueva_factura,
#                         producto=producto,
#                         cantidad=cantidad,
#                         precio_unitario=producto.precio_venta,
#                         subtotal=p_subtotal
#                     )

#                     # Descontar Stock
#                     producto.stock -= cantidad
#                     producto.save()

#                     total_subtotal += p_subtotal

#                 # 3. Cálculos Finales de la Factura
#                 impuesto = total_subtotal * tasa_iva
#                 total_final = total_subtotal + impuesto

#                 # Actualizamos la cabecera con los totales reales
#                 nueva_factura.subtotal = total_subtotal
#                 nueva_factura.igv = impuesto
#                 nueva_factura.total = total_final
#                 nueva_factura.save()

#             return redirect('/facturas') # O a la vista de impresión

#         except Exception as e:
#             print(f"Error en facturación: {e}")
#             return redirect('/index')
            
#     return redirect('facturas/index.html')

# def billing(request):
#     # Obtenemos las últimas 5 facturas
#     facturas = Factura.objects.all().order_by('-fecha_emision')[:5]
    
#     # Obtenemos los clientes para la sección "Billing Information"
#     clientes_billing = Cliente.objects.filter(activo=True)[:3]
    
#     # Calculamos algunos totales para las tarjetas superiores (opcional)
#     total_ingresos = sum(f.total for f in Factura.objects.filter(estado='Pagado'))

#     context = {
#         'facturas': facturas,
#         'clientes': clientes_billing,
#         'total_ingresos': total_ingresos,
#     }
#     return render(request, 'pages/billing.html', context)

# def nueva_venta(request):
#     productos_disponibles = Producto.objects.filter(activo=True, stock__gt=0)
#     clientes = Cliente.objects.all()
#     tipo = tipo_documnento.objects.all()
#     context = {
#         'segment': 'nueva_venta',
#         'productos': productos_disponibles,
#         'clientes': clientes,
#         'tipos_documento': tipo
#     }
#     return render(request, 'pages/ventas.html', context)

# def detalle_factura(request, factura_id):
#     # Buscamos la factura o devolvemos 404 si no existe
#     factura = get_object_or_404(Factura, id=factura_id)
#     # Filtramos los productos que se vendieron en esa factura específica
#     detalles = DetalleFactura.objects.filter(factura=factura)
    
#     context = {
#         'segment': 'facturas',
#         'factura': factura,
#         'detalles': detalles
#     }
#     return render(request, 'pages/detalle_factura.html', context)

# def virtual_reality(request):
#     context = {
#         'segment': 'virtual_reality'
#     }
#     return render(request, 'pages/virtual-reality.html', context)

# def rtl(request):
#     context = {
#         'segment': 'rtl'
#     }
#     return render(request, 'pages/rtl.html', context)

# def notifications(request):
#     context = {
#         'segment': 'notifications'
#     }
#     return render(request, 'pages/notifications.html', context)

# def profile(request):
#     context = {
#         'segment': 'profile'
#     }
#     return render(request, 'pages/profile.html', context)


# def registrar_compra(request):
#     if request.method == 'POST':
#         producto_id = request.POST.get('producto_id')
#         cantidad_comprada = int(request.POST.get('cantidad'))
#         costo_unitario = Decimal(request.POST.get('precio_compra'))

#         try:
#             with transaction.atomic():
#                 producto = Producto.objects.get(id=producto_id)
                
#                 # Actualizamos el stock (Trazabilidad de entrada)
#                 producto.stock += cantidad_comprada
                
#                 # Opcional: Actualizamos el precio de compra si cambió
#                 producto.precio_compra = costo_unitario
#                 producto.save()
                
#                 # Aquí podrías crear un modelo 'IngresoStock' para historial detallado
#                 print(f"Entrada de stock: {producto.nombre} +{cantidad_comprada}")
                
#             return redirect('/productos')
#         except Exception as e:
#             print(f"Error en compra: {e}")
#             return redirect('/index')

# def editar_perfil(request):
#     pass

# def user_logout_view(request):
#   logout(request)
#   return redirect('login')