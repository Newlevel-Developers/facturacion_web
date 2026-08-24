import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count, Q, F
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import login as auth_login, logout

from facturacion.forms import LoginForm
from facturacion.models import Factura, IngresoStock, Cliente, Producto, Proveedor


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            print('Login successful!')
            return redirect('/dashboard_facturacion')
        else:
            print("Login failed!")
    else:
        form = LoginForm()
  
    context = {'form': form}
    return render(request, 'pages/sign-in.html', context)


def dashboard_facturacion(request):
    today = timezone.now().date()
    inicio_mes = today.replace(day=1)
    
    # --- 1. MÉTRICAS PRINCIPALES ---
    
    # Ventas de Hoy (Estado PAGADO y campo fecha_emision)
    ventas_hoy_query = Factura.objects.filter(
        fecha_emision__date=today, 
        estado='PAGADO'
    ).aggregate(total=Sum('total'))
    ventas_hoy = ventas_hoy_query['total'] or 0.0

    # Ventas de Ayer
    ayer = today - timezone.timedelta(days=1)
    ventas_ayer_query = Factura.objects.filter(
        fecha_emision__date=ayer, 
        estado='PAGADO'
    ).aggregate(total=Sum('total'))
    ventas_ayer = ventas_ayer_query['total'] or 0.0

    # Porcentaje de cambio en ventas diarias
    if ventas_ayer > 0:
        porcentaje_ventas = round(((ventas_hoy - ventas_ayer) / ventas_ayer) * 100, 1)
    else:
        porcentaje_ventas = 100.0 if ventas_hoy > 0 else 0.0

    # Por Cobrar (Pendientes)
    cuentas_por_cobrar = Factura.objects.filter(estado='PENDIENTE').aggregate(
        total=Sum('total'),
        cantidad=Count('id')
    )
    por_cobrar = cuentas_por_cobrar['total'] or 0.0
    facturas_pendientes = cuentas_por_cobrar['cantidad'] or 0

    # Facturas del Mes Actual vs Mes Anterior
    facturas_mes = Factura.objects.filter(fecha_emision__date__gte=inicio_mes).count()
    
    primer_dia_mes_anterior = (inicio_mes - timezone.timedelta(days=1)).replace(day=1)
    ultimo_dia_mes_anterior = inicio_mes - timezone.timedelta(days=1)
    facturas_mes_anterior = Factura.objects.filter(
        fecha_emision__date__gte=primer_dia_mes_anterior,
        fecha_emision__date__lte=ultimo_dia_mes_anterior
    ).count()

    if facturas_mes_anterior > 0:
        porcentaje_facturas = round(((facturas_mes - facturas_mes_anterior) / facturas_mes_anterior) * 100, 1)
    else:
        porcentaje_facturas = 100.0 if facturas_mes > 0 else 0.0

    # Egresos Hoy (Suma de cantidad * precio_compra en IngresoStock)
    egresos_query = IngresoStock.objects.filter(
        fecha_ingreso__date=today
    ).aggregate(
        total=Sum(F('cantidad') * F('precio_compra'))
    )
    egresos_hoy = egresos_query['total'] or 0.0

    # --- 2. DATOS DEL GRÁFICO MENSUAL ---
    selected_year = int(request.GET.get('year', today.year))
    
    ventas_mensuales = []
    for mes in range(1, 13):
        monto_mes = Factura.objects.filter(
            fecha_emision__year=selected_year,
            fecha_emision__month=mes,
            estado='PAGADO'
        ).aggregate(total=Sum('total'))['total'] or 0.0
        ventas_mensuales.append(float(monto_mes))

    # --- 3. LISTADOS Y ACTIVIDAD RECIENTE ---
    facturas_recientes = Factura.objects.select_related('cliente').order_by('-fecha_emision')[:10]
    actividades_recientes = Factura.objects.select_related('cliente').order_by('-fecha_emision')[:5]

    context = {
        'today': today,
        'selected_year': selected_year,
        'ventas_hoy': ventas_hoy,
        'porcentaje_ventas': porcentaje_ventas,
        'por_cobrar': por_cobrar,
        'facturas_pendientes': facturas_pendientes,
        'facturas_mes': facturas_mes,
        'porcentaje_facturas': porcentaje_facturas,
        'egresos_hoy': egresos_hoy,
        'chart_data_json': json.dumps(ventas_mensuales, cls=DjangoJSONEncoder),
        'facturas_recientes': facturas_recientes,
        'actividades_recientes': actividades_recientes,
    }

    return render(request, 'pages/dashboard.html', context)


def user_logout_view(request):
    logout(request)
    return redirect('login')


def profile(request):
    context = {
        'segment': 'profile'
    }
    return render(request, 'pages/profile.html', context)


def editar_perfil(request):
    pass