from django.db import models

class Proveedor(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('J', 'J - Jurídico'),
        ('V', 'V - Venezolano'),
        ('E', 'E - Extranjero'),
        ('G', 'G - Gubernamental'),
    ]

    tipo_documento = models.CharField(
        max_length=1, 
        choices=TIPO_DOCUMENTO_CHOICES, 
        default='J'
    )
    rif_cedula = models.CharField(max_length=20, unique=True, verbose_name="RIF / Cédula")
    nombre_razon_social = models.CharField(max_length=150, verbose_name="Nombre / Razón Social")
    contacto_persona = models.CharField(max_length=100, null=True, blank=True, verbose_name="Persona de Contacto")
    email = models.EmailField(max_length=254, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.TextField(null=True, blank=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compras_proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.tipo_documento}-{self.rif_cedula} | {self.nombre_razon_social}"