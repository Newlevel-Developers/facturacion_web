from django.shortcuts import render, redirect
from facturacion.models import Producto, Categoria  

def productos(request):
    
    productos = Producto.objects.all()   
    categorias = Categoria.objects.all()       
    context = {
        'segment': 'productos',
        'productos': productos,
        'categorias': categorias
    }
    return render(request, 'Productos/index.html', context)

def crear_producto(request):
    if request.method == 'POST':
        # 1. Captura de todos los campos del formulario
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_minimo = request.POST.get('stock_minimo')
        categoria_id = request.POST.get('categoria')
        
        # Manejo del checkbox (booleanos en Django)
        activo = True if request.POST.get('activo') == 'on' else False
        
        # 2. Captura de la imagen (requiere request.FILES)
        imagen = request.FILES.get('imagen')

        try:
            # 3. Creación con los nombres exactos de tu modelo/base de datos
            new_producto = Producto.objects.create(
                codigo=codigo,                     # Faltaba
                nombre=nombre,
                descripcion=descripcion,
                precio_compra=precio_compra,       # Tu SQL usa precio_compra
                precio_venta=precio_venta,         # Tu SQL usa precio_venta
                stock=stock,                       # Faltaba
                stock_minimo=stock_minimo,         # Faltaba
                imagen=imagen,                     # Faltaba manejar el archivo
                activo=activo,                     # Faltaba
                categoria_id=categoria_id
            )
            
            return redirect('/productos')
            
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return redirect('/index')
    else:
        return redirect('/index')