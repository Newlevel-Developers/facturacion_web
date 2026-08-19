from django.db import models

class Proveedor(models.Model):
    rif_cedula = models.CharField(max_length=20, unique=True)
    nombre_razon_social = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compras_proveedor'

    def __str__(self):
        return self.nombre_razon_social