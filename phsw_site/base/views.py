from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


# ---------------/ Usuário


@login_required
def criar_usuario(request):
    return render(request, 'usuario/criar_usuario.html', context={'arg': "arg", })


@login_required
def editar_usuarios(request):
    return render(request, 'usuario/editar_usuario.html', context={'arg': "arg", })


# ---------------/ Empresa

@login_required
def criar_empresa(request):
    return render(request, 'usuario/criar_empresa.html', context={'arg': "arg", })


@login_required
def editar_empresa(request):
    return render(request, 'usuario/editar_empresa.html', context={'arg': "arg", })
