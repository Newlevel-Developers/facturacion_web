from django.db import models

class MetodoPago(models.Model):
    TIPO_METODO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('PAGO_MOVIL', 'Pago Móvil'),
        ('PUNTO_VENTA', 'Punto de Venta / Tarjeta'),
        ('DIVISA', 'Moneda Extranjera / Zelle / USDT'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Método")
    codigo = models.CharField(max_length=20, unique=True, help_text="Código corto (ej: PM, EFECT)")
    tipo = models.CharField(max_length=20, choices=TIPO_METODO_CHOICES, default='EFECTIVO', verbose_name="Tipo de Método")
    requiere_referencia = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'facturas_metodopago'
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class PagoFactura(models.Model):
    # Usar string 'Factura' evita problemas de importación circular
    factura = models.ForeignKey('Factura', on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT, related_name='pagos_realizados')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    banco_origen = models.CharField(max_length=80, blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'facturas_pagofactura'
        verbose_name = "Pago de Factura"
        verbose_name_plural = "Pagos de Facturas"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"{self.metodo_pago.nombre} - {self.monto} (Factura #{self.factura_id})"