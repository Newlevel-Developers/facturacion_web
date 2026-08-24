from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False), name='index'),
    path('index', views.index, name="index"),
    
    #Usuarios
    path('usuarios/', views.usuarios, name="usuarios"),
    path('registrar_usuario/', views.registrar_usuario, name="registrar_usuario"),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
    path('editar_rol/', views.editar_rol, name='editar_rol'),
    path('eliminar_rol/', views.eliminar_rol, name='eliminar_rol'),
    
    #Perfil
    path('profile/', views.profile, name="profile"),
    path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    
    #Productos para inventario
    path('productos/', views.productos, name="productos"),
    path('crear_producto/', views.crear_producto, name="crear_producto"),
    path('editar_producto/<int:id>/', views.editar_producto, name="editar_producto"),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/exportar/', views.exportar_productos_excel, name='exportar_productos_excel'),
    path('productos/importar/', views.importar_productos_excel, name='importar_productos_excel'),
    
    #Categoria del producto
    path('crear_categoria/', views.crear_categoria, name="crear_categoria"),
    path('editar_categoria', views.editar_categoria, name="editar_categoria"),
    path('eliminar_categoria', views.eliminar_categoria, name="eliminar_categoria"),
    
    #Clientes
    path('clientes/', views.clientes, name="clientes"),
    path('registrar_clientes/', views.registrar_clientes, name="registrar_clientes"),
    path('editar_cliente/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name="eliminar_cliente"),
    
    #Proveedor
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # Facturación
    path('facturas/', views.facturas, name="facturas"),
    path('crear_factura/', views.crear_factura, name="crear_factura"),
    path('detalle_factura/<int:factura_id>/', views.detalle_factura, name="detalle_factura"),
    path('billing/', views.billing, name="billing"),
    path('anular_factura/<int:factura_id>/', views.anular_factura , name='anular_factura'),
    path('facturas/pdf/<int:id>/', views.generar_factura_pdf, name="generar_factura_pdf"),

    # Compras / Trazabilidad de entrada
    path('registrar_compra/', views.registrar_compra, name="registrar_compra"),
    
    # venta / Trazabilidad de salida
    path('nueva_venta/', views.nueva_venta, name="nueva_venta"),

    
    # Authentication
    path('login/', views.login, name='login'),

    path('logout/', views.user_logout_view, name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)