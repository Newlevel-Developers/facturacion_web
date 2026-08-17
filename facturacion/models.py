from django.db import models


class tipo_documnento(models.Model):
    tipo = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'tipo_documento'
        
    def __str__(self):
        return self.tipo
    
class Cliente(models.Model):
    tipo_documento = models.ForeignKey(tipo_documnento, on_delete=models.CASCADE)
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
        
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    class Meta:
        db_table = 'productos_categoria'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = 'productos_producto'

    def __str__(self):
        return self.nombre
    
from django.contrib.auth.models import User

class Factura(models.Model):
    numero_factura = models.CharField(max_length=20)
    tipo_comprobante = models.CharField(max_length=10)
    fecha_emision = models.DateTimeField()
    fecha_pago = models.DateTimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10)
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