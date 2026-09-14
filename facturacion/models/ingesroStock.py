from django.db import models
from django.contrib.auth.models import User
from .product import Producto
from .provider import Proveedor
from .payment import MetodoPago  # Importamos MetodoPago

class IngresoStock(models.Model):
    ESTADO_CHOICES = [
        ('PAGADO', 'Pagado'),
        ('PENDIENTE', 'Pendiente'),
        ('CANCELADO', 'Cancelado'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # cantidad * precio_compra
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PAGADO')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'compras_ingresostock'


class PagoProveedor(models.Model):
    ingreso = models.ForeignKey(IngresoStock, on_delete=models.CASCADE, related_name='pagos_proveedor')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'compras_pagoproveedor'