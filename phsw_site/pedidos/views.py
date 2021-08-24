from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade
from django.core.paginator import Paginator

from .models import ItemForm


@login_required
def fazer_pedido(request):
    categoria_queryset = facade.buscar_itens_por_categoria()
    if request.method != 'POST':
        return render(request, 'pedidos/fazer_pedido.html', context={'categorias': categoria_queryset})

    if request.method == 'POST':
        facade.fazer_pedido(request)
        return render(request, 'pedidos/fazer_pedido.html', context={'categorias': categoria_queryset})


@login_required
def ver_pedidos(request):
    pedidos_queryset = facade.buscar_pedidos(request)
    paginator = Paginator(pedidos_queryset, 3)
    page = request.GET.get('page')
    pedidos_paginator = paginator.get_page(page)
    return render(request, 'pedidos/ver_pedidos.html', context={'pedidos': pedidos_paginator})


@login_required
def ver_pedido(request):
    pedido = facade.buscar_pedido(request)
    return render(request, 'pedidos/ver_pedido.html', context={'pedido': pedido})


@login_required
def editar_itens(request):
    itens = facade.buscar_todos_os_itens_por_categoria()
    if request.method == 'POST':  # Adicionando item com ModelForms
        form = ItemForm(request.POST, request.FILES)
        if not form.is_valid():
            form = ItemForm(request.POST)
            messages.error(request, "Erro ao enviar formulario.")
            return render(request, 'pedidos/editar_itens.html', context={'categorias': itens, 'form': form})
        form.save()
        messages.success(request, f'Item {request.POST.get("verbose_name")} criado com sucesso.')
        imagem = request.POST.get('imagem')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        unidade = request.POST.get('unidade')
        # facade.editar_itens(request)  # Editando itens.
    form = ItemForm()
    return render(request, 'pedidos/editar_itens.html', context={'categorias': itens, 'form': form})


