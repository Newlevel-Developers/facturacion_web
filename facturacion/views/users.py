from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group, Permission


def usuarios(request):
    usuarios = User.objects.all()
    roles = Group.objects.all()
    permisos = Permission.objects.all().select_related('content_type')
    usuarios_activos = usuarios.filter(is_active=True)
    if usuarios.exists():
        ultimo_registro = usuarios.latest('date_joined')
    else:
        ultimo_registro = None
        
    context = {
        'segment': 'usuarios',
        'usuarios_activos': usuarios_activos,
        'ultimo_registro': ultimo_registro,
        'roles': roles,
        'permisos':permisos,
        'usuarios': usuarios
    }
    return render(request, 'pages/usuarios.html', context)

def registrar_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not email or not password or not first_name or not last_name:
            print("All fields are required!")
            return redirect('/index')
        try:
            new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            new_user.save()
            print('User created successfully!')
            return redirect('/usuarios')
        except Exception as e:
            print(f"Error creating user: {e}")
            return redirect('/index')
    else:
        print("Invalid request method!")
        return redirect('/usuarios')

def editar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')
            
            # Validación simple
            if not all([user.first_name, user.last_name, user.email, user.username]):
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect('/tables')

            user.save()
            messages.success(request, '¡Usuario actualizado correctamente!')
            return redirect('/tables')
            
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        
        return redirect('/tables')
    
    return redirect('/index')

def editar_perfil(request):
    pass

def crear_rol(request):
    if request.method == 'POST':
        nombre = request.POST.get('name')
        # getlist obtiene todos los IDs de los permisos seleccionados
        permisos_ids = request.POST.getlist('permissions') 

        if not nombre:
            messages.error(request, "El nombre del rol es obligatorio.")
            return redirect('/usuarios')

        # Verificar si el rol ya existe
        if Group.objects.filter(name__iexact=nombre).exists():
            messages.warning(request, f"El rol '{nombre}' ya existe.")
            return redirect('/usuarios')

        try:
            # Crear el grupo (rol)
            nuevo_rol = Group.objects.create(name=nombre)
            
            # Asignar los permisos seleccionados al rol
            if permisos_ids:
                permisos = Permission.objects.filter(id__in=permisos_ids)
                nuevo_rol.permissions.set(permisos)

            messages.success(request, f"¡Rol '{nombre}' creado con sus permisos exitosamente!")
        except Exception as e:
            messages.error(request, f"Error al crear el rol: {e}")

        return redirect('/usuarios')

    return redirect('/usuarios')

def editar_rol(request):
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        nuevo_nombre = request.POST.get('name')
        permisos_ids = request.POST.getlist('permissions')

        if not role_id or not nuevo_nombre:
            messages.error(request, "Debes seleccionar un rol y proporcionar un nombre.")
            return redirect('/usuarios')

        try:
            rol = Group.objects.get(id=role_id)
            
            # Verificar nombre duplicado
            if Group.objects.filter(name__iexact=nuevo_nombre).exclude(id=role_id).exists():
                messages.warning(request, f"Ya existe otro rol llamado '{nuevo_nombre}'.")
                return redirect('/usuarios')

            rol.name = nuevo_nombre
            rol.save()

            # Actualizar la lista de permisos (reemplaza los anteriores por los nuevos)
            permisos = Permission.objects.filter(id__in=permisos_ids)
            rol.permissions.set(permisos)

            messages.success(request, "¡Rol y permisos actualizados correctamente!")
        except Group.DoesNotExist:
            messages.error(request, "El rol seleccionado no existe.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el rol: {e}")

        return redirect('/usuarios')

    return redirect('/usuarios')

def eliminar_rol(request):
    if request.method == 'POST':
        role_id = request.POST.get('role_id')

        if not role_id:
            messages.error(request, "Debes seleccionar un rol para eliminar.")
            return redirect('/usuarios')

        try:
            rol = Group.objects.get(id=role_id)
            nombre_rol = rol.name
            rol.delete()
            messages.success(request, f"¡El rol '{nombre_rol}' fue eliminado con éxito!")
        except Group.DoesNotExist:
            messages.error(request, "El rol seleccionado no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el rol: {e}")

        return redirect('/usuarios')

    return redirect('/usuarios')