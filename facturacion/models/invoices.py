from django.contrib.auth.models import User
from django.db import models
from .client import Cliente
from .product import Producto
class Factura(models.Model):
    ESTADO_CHOICES = [
        ('PAGADO', 'Pagado'),
        ('PENDIENTE', 'Pendiente'),
        ('CANCELADO', 'Cancelado'),
    ]
    numero_factura = models.CharField(max_length=20)
    tipo_comprobante = models.CharField(max_length=10)
    fecha_emision = models.DateTimeField()
    fecha_pago = models.DateTimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE'
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'facturas_factura'

class DetalleFactura(models.Model):
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    class Meta:
        db_table = 'facturas_detallefactura'