import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker

# Importa tus modelos de acuerdo a la ubicación real en tu proyecto
from facturacion.models import (
    tipo_documnento,
    Cliente,
    Categoria,
    Producto,
    Factura,
    DetalleFactura,
    Proveedor,
    IngresoStock
)

fake = Faker(['es_ES', 'es_CO', 'es_MX'])  # Genera datos en español


class Command(BaseCommand):
    help = "Pobla la base de datos con información realista de una tienda de tecnología"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando la generación de datos de tecnología..."))

        # ----------------------------------------------------
        # 1. USUARIOS (Vendedores / Administradores)
        # ----------------------------------------------------
        self.stdout.write("1. Creando usuarios vendedores...")
        usuarios = []
        for i in range(1, 6):
            username = f"vendedor_{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": f"vendedor{i}@techstore.com",
                    "is_staff": True
                }
            )
            if created:
                user.set_password("Admin12345")
                user.save()
            usuarios.append(user)

        # ----------------------------------------------------
        # 2. PROVEEDORES
        # ----------------------------------------------------
        self.stdout.write("2. Creando proveedores de tecnología...")
        proveedores_demo = [
            ("J-30012345-0", "TechSupply Wholesale C.A.", "contacto@techsupply.com", "+58 212 5550101"),
            ("J-30098765-1", "Importadora Global Tech S.A.", "ventas@globaltech.com", "+58 212 5550102"),
            ("J-40011223-3", "Distribuidora Asus & Hardware R.L.", "pedidos@ashardware.com", "+58 241 5550103"),
            ("J-40044556-4", "Comercializadora Computo Express", "info@computoexpress.com", "+58 261 5550104")
        ]
        
        proveedores = []
        for rif, razon_social, email_prov, tlf in proveedores_demo:
            proveedor, _ = Proveedor.objects.get_or_create(
                rif_cedula=rif,
                defaults={
                    "nombre_razon_social": razon_social,
                    "email": email_prov,
                    "telefono": tlf,
                    "direccion": fake.address().replace("\n", ", "),
                    "activo": True
                }
            )
            proveedores.append(proveedor)

        # ----------------------------------------------------
        # 3. TIPOS DE DOCUMENTO
        # ----------------------------------------------------
        self.stdout.write("3. Creando tipos de documentos...")
        tipos_doc_nombres = ["DNI", "RUC", "Pasaporte", "Cedula de Ciudadania"]
        tipos_doc_objs = []
        for tipo in tipos_doc_nombres:
            doc, _ = tipo_documnento.objects.get_or_create(tipo=tipo)
            tipos_doc_objs.append(doc)

        # ----------------------------------------------------
        # 4. CLIENTES (50 Clientes)
        # ----------------------------------------------------
        self.stdout.write("4. Generando 50 clientes...")
        clientes = []
        for _ in range(50):
            td = random.choice(tipos_doc_objs)
            # RUC/DNI simulación
            num_doc = fake.numerify("8765####") if td.tipo == "DNI" else fake.numerify("20###########")
            
            cliente = Cliente.objects.create(
                tipo_documento=td,
                numero_documento=num_doc,
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                email=fake.unique.email(),
                telefono=fake.numerify("9########"),
                direccion=fake.address().replace("\n", ", "),
                activo=True
            )
            clientes.append(cliente)

        # ----------------------------------------------------
        # 5. CATEGORÍAS Y PRODUCTOS DE TECNOLOGÍA
        # ----------------------------------------------------
        self.stdout.write("5. Creando categorías y catálogo de productos...")
        
        catalogo_tech = {
            "Laptops y Laptops Gamer": [
                ("ASUS ROG Strix G16", "Intel i7-13650HX, RTX 4060, 16GB RAM, 512GB SSD", 1100.00, 1450.00),
                ("MacBook Air M2", "Apple M2 8-core CPU, 8-core GPU, 8GB Unified, 256GB SSD", 900.00, 1199.00),
                ("Lenovo Legion Pro 5", "AMD Ryzen 7 7745HX, RTX 4070, 32GB RAM, 1TB SSD", 1350.00, 1750.00),
                ("Dell XPS 13", "Intel Core Ultra 7, 16GB LPDDR5x, 512GB SSD OLED", 1200.00, 1599.00),
                ("HP Pavilion 15", "AMD Ryzen 5 5500U, 8GB RAM, 256GB SSD", 420.00, 580.00),
            ],
            "Componentes de PC": [
                ("NVIDIA RTX 4080 Super 16GB", "Tarjeta de video para juegos a 4K con Ray Tracing", 950.00, 1199.00),
                ("AMD Ryzen 7 7800X3D", "El mejor procesador para gaming, 8 núcleos 16 hilos", 330.00, 420.00),
                ("Intel Core i9-14900K", "Procesador de 24 núcleos hasta 6.0 GHz LGA1700", 500.00, 620.00),
                ("RAM Corsair Vengeance DDR5 32GB", "Kit 2x16GB 6000MHz CL30 RGB", 100.00, 145.00),
                ("SSD Samsung 990 PRO 2TB", "PCIe 4.0 NVMe M.2 con lecturas hasta 7450 MB/s", 140.00, 195.00),
                ("Fuente ASUS ROG Thor 1000W", "80 Plus Platinum, Fuente de poder modular con pantalla OLED", 240.00, 310.00),
            ],
            "Periféricos y Monitores": [
                ("Monitor Gaming LG Ultragear 27''", "27 IPS QHD 165Hz 1ms G-Sync Compatible", 220.00, 310.00),
                ("Teclado Mecánico Logitech G Pro X", "Switches GX Blue clicky, RGB LIGHTSYNC", 90.00, 135.00),
                ("Mouse Razer DeathAdder V3 Pro", "Mouse inalámbrico ultra liviano 63g 30K DPI", 100.00, 149.00),
                ("Audífonos HyperX Cloud II", "Sonido Surround 7.1 con cancelación de ruido", 55.00, 85.00),
            ],
            "Smartphones y Gadgets": [
                ("Samsung Galaxy S24 Ultra 512GB", "Titanium Gray, S-Pen incluido, cámara 200MP", 1050.00, 1399.00),
                ("iPhone 15 Pro Max 256GB", "Titanio Natural, chip A17 Pro, conector USB-C", 1100.00, 1420.00),
                ("Smartwatch Garmin Fenix 7X Pro", "Reloj multideporte con carga solar y linterna LED", 650.00, 850.00),
                ("Tablet Apple iPad Air M2 11''", "Wi-Fi 128GB - Gris Espacial", 480.00, 629.00),
            ]
        }

        productos_creados = []
        for cat_nombre, lista_prods in catalogo_tech.items():
            categoria_obj, _ = Categoria.objects.get_or_create(
                nombre=cat_nombre,
                defaults={"descripcion": f"Todos los artículos y novedades sobre {cat_nombre}"}
            )

            for prod in lista_prods:
                nombre, desc, p_compra, p_venta = prod
                stock_inicial = random.randint(15, 60)

                p = Producto.objects.create(
                    codigo=f"TEC-{random.randint(10000, 99999)}",
                    nombre=nombre,
                    descripcion=desc,
                    precio_compra=Decimal(str(p_compra)),
                    precio_venta=Decimal(str(p_venta)),
                    stock=stock_inicial,
                    stock_minimo=3,
                    activo=True,
                    categoria=categoria_obj
                )
                productos_creados.append(p)

                # ----------------------------------------------------
                # 6. HISTORIAL DE INGRESO DE STOCK
                # ----------------------------------------------------
                IngresoStock.objects.create(
                    producto=p,
                    proveedor=random.choice(proveedores),
                    usuario=random.choice(usuarios),
                    cantidad=stock_inicial,
                    precio_compra=Decimal(str(p_compra)),
                    observacion="Carga inicial de inventario / Importación"
                )

        # ----------------------------------------------------
        # 7. FACTURAS Y DETALLES (80 Facturas emitidas)
        # ----------------------------------------------------
        self.stdout.write("7. Generando 80 facturas con sus detalles...")

        tipos_comprobante = ["Factura", "Boleta"]
        estados = ["Pagada", "Pendiente", "Anulada"]

        for i in range(1, 81):
            fecha_emision = timezone.now() - timedelta(days=random.randint(1, 180))
            estado = random.choice(estados)
            fecha_pago = fecha_emision + timedelta(days=random.randint(0, 5)) if estado == "Pagada" else None

            # Seleccionar cliente y usuario vendedor
            cli = random.choice(clientes)
            usr = random.choice(usuarios)

            # Instanciamos la factura temporalmente (Subtotal/Total en 0)
            factura = Factura.objects.create(
                numero_factura=f"F001-{i:06d}",
                tipo_comprobante=random.choice(tipos_comprobante),
                fecha_emision=fecha_emision,
                fecha_pago=fecha_pago,
                subtotal=Decimal("0.00"),
                igv=Decimal("0.00"),
                total=Decimal("0.00"),
                estado=estado,
                cliente=cli,
                usuario=usr
            )

            # Agregar de 1 a 4 productos a la factura
            prods_factura = random.sample(productos_creados, k=random.randint(1, 4))
            subtotal_factura = Decimal("0.00")

            for prod in prods_factura:
                cant = random.randint(1, 3)
                p_unitario = prod.precio_venta
                subtotal_item = Decimal(cant) * p_unitario

                DetalleFactura.objects.create(
                    cantidad=cant,
                    precio_unitario=p_unitario,
                    subtotal=subtotal_item,
                    producto=prod,
                    factura=factura
                )
                subtotal_factura += subtotal_item

            # Cálculo de Impuestos (18% IGV / IVA estándar)
            igv_calculado = round(subtotal_factura * Decimal("0.18"), 2)
            total_calculado = subtotal_factura + igv_calculado

            # Actualizar totales en la factura principal
            factura.subtotal = subtotal_factura
            factura.igv = igv_calculado
            factura.total = total_calculado
            factura.save()

        self.stdout.write(self.style.SUCCESS("¡Base de datos cargada correctamente con éxito! 🚀"))