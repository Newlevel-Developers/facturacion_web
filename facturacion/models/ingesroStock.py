from django.contrib.auth.models import User
from django.db import models

from .product import Producto
from .provider import Proveedor


class IngresoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, null=True, blank=True
    )
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'compras_ingresostock'

    def __str__(self):
        return f"Ingreso #{self.id} - {self.producto.nombre}"