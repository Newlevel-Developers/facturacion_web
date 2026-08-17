from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False), name='index'),
    path('index', views.index, name="index"),
    path('usuarios/', views.usuarios, name="usuarios"),
    path('registrar_usuario/', views.registrar_usuario, name="registrar_usuario"),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('billing/', views.billing, name="billing"),
    # path('virtual-reality/', views.virtual_reality, name="virtual_reality"),
    # path('rtl/', views.rtl, name="rtl"),
    # path('notifications/', views.notifications, name="notifications"),
    path('profile/', views.profile, name="profile"),
    path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    path('productos/', views.productos, name="productos"),
    path('crear_producto/', views.crear_producto, name="crear_producto"),
    path('clientes/', views.clientes, name="clientes"),
    path('registrar_clientes/', views.registrar_clientes, name="registrar_clientes"),
    # path('charts/', views.charts, name="charts"),
    
    # Facturación
    path('facturas/', views.facturas, name="facturas"),
    path('crear_factura/', views.crear_factura, name="crear_factura"),

    # Compras / Trazabilidad de entrada
    path('registrar_compra/', views.registrar_compra, name="registrar_compra"),
    
    # venta / Trazabilidad de salida
    path('nueva_venta/', views.nueva_venta, name="nueva_venta"),

    path('detalle_factura/<int:factura_id>/', views.detalle_factura, name="detalle_factura"),
    
    # Authentication
    path('login/', views.login, name='login'),

     path('logout/', views.user_logout_view, name='logout'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)