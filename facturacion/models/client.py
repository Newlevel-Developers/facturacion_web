from django.db import models

class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'tipo_documento'
        
    def __str__(self):
        return self.tipo
    
class Cliente(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    numero_documento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'clientes_cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"