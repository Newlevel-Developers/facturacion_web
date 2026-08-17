from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def usuarios(request):
    usuarios = User.objects.all()
    context = {
        'segment': 'usuarios',
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
            return redirect('/tables')
        except Exception as e:
            print(f"Error creating user: {e}")
            return redirect('/index')
    else:
        print("Invalid request method!")
        return redirect('/index')

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


def profile(request):
    context = {
        'segment': 'profile'
    }
    return render(request, 'pages/profile.html', context)


def editar_perfil(request):
    pass
