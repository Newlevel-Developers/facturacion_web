from django.contrib.auth import login as auth_login, logout
from facturacion.forms import LoginForm
from django.shortcuts import redirect
from django.shortcuts import render


def login(request):
  if request.method == 'POST':
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      auth_login(request, user)
      print('Login successful!')
      return redirect('/index')
    else:
      print("Login failed!")
  else:
    form = LoginForm()
  
  context = {'form': form}
  return render(request, 'pages/sign-in.html', context)


def index(request):
    context = {
        'segment': 'dashboard'
    }
    return render(request, 'pages/index.html', context)


def user_logout_view(request):
  logout(request)
  return redirect('login')

def profile(request):
    context = {
        'segment': 'profile'
    }
    return render(request, 'pages/profile.html', context)
  
def editar_perfil(request):
      pass
