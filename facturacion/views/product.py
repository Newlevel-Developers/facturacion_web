from django.shortcuts import render, redirect,get_object_or_404
from facturacion.models import Producto, Categoria  
from django.contrib import messages
from django.db.models import F
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('facturacion.view_producto', raise_exception=True)
def productos(request):
    productos = Producto.objects.all()   
    productos_activos =  productos.filter(activo=True)
    productos_stock_bajo = productos.filter(stock__lte=F('stock_minimo'))
    context = {
        'segment': 'productos',
        'productos': productos,
        'productos_activos': productos_activos, 
        'productos_stock_bajo': productos_stock_bajo,  
    }
    return render(request, 'Productos/index.html', context)

@permission_required('facturacion.add_producto', raise_exception=True)
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

@permission_required('facturacion.change_producto', raise_exception=True)
def editar_producto(request, id):
    # 1. Obtenemos el producto a editar
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        # 2. Obtenemos los datos enviados por el formulario
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_minimo = request.POST.get('stock_minimo')
        descripcion = request.POST.get('descripcion')
        
        # El checkbox sólo se envía en el POST si está marcado (retorna 'on')
        activo = 'activo' in request.POST 

        # 3. Actualizamos los atributos del producto
        producto.codigo = codigo
        producto.nombre = nombre
        
        # Asignamos la categoría relacionada
        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            producto.categoria = categoria
            
        producto.precio_compra = precio_compra
        producto.precio_venta = precio_venta
        producto.stock = stock
        producto.stock_minimo = stock_minimo
        producto.descripcion = descripcion
        producto.activo = activo

        # 4. Manejo de la imagen (solo si el usuario subió una nueva archivo)
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        # 5. Guardamos las modificaciones en la base de datos
        producto.save()

        messages.success(request, f'El producto "{producto.nombre}" fue actualizado correctamente.')
        return redirect('productos')  # Cambia 'lista_productos' por la url/vista a donde quieras redirigir

    # Si la petición no es POST, simplemente redirigimos a la lista
    return redirect('productos')

@permission_required('facturacion.delete_producto', raise_exception=True)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, 'Producto eliminado con éxito.')
    return redirect('productos')

@permission_required('facturacion.view_categoria', raise_exception=True)
def categoria(request):
    categorias = Categoria.objects.all()
    total_categorias = categorias.count()
    context = { 
            'total_categorias': total_categorias,
            'categorias': categorias
        }
    return render(request, 'Productos/index.html', context)
    
@permission_required('facturacion.add_categoria', raise_exception=True)
def crear_categoria(request):
    if request.method == 'POST':

            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
    
            try:
                new_categoria = Categoria.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                )
                
                return redirect('/productos')
                
            except Exception as e:
                print(f"Error al crear producto: {e}")
                return redirect('/index')
    else:
            return redirect('/index')       

@permission_required('facturacion.change_categoria', raise_exception=True)
def editar_categoria(request):
    if request.method == 'POST':
        # 1. Obtenemos el ID de la categoría enviado por el modal
        categoria_id = request.POST.get('categoria_id')
        
        # 2. Buscamos la categoría en la base de datos
        categoria = get_object_or_404(Categoria, id=categoria_id)

        # 3. Obtenemos los nuevos datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # 4. Actualizamos y guardamos
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.save()

        messages.success(request, f'La categoría "{categoria.nombre}" fue actualizada correctamente.')
        return redirect('productos')

    return redirect('productos')

@permission_required('facturacion.delete_categoria', raise_exception=True)
def eliminar_categoria(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        categoria = get_object_or_404(Categoria, id=categoria_id)
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('productos')
    return redirect('productos')