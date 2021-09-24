from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade
from django.core.paginator import Paginator

from .forms import ItemForm


@login_required
def make_order(request):
    category_queryset = facade.user_category_items_queryset(request)
    if request.method != 'POST':
        return render(request, 'orders/make_order.html', context={'categories': category_queryset})

    if request.method == 'POST':
        facade.make_order(request)
        return render(request, 'orders/make_order.html', context={'categories': category_queryset})


@login_required
def view_orders(request):
    orders_queryset = facade.get_orders(request)
    paginator = Paginator(orders_queryset, 3)
    page = request.GET.get('page')
    orders_paginator = paginator.get_page(page)
    return render(request, 'orders/view_orders.html', context={'orders': orders_paginator})


@login_required
def view_order(request):
    order = facade.get_order(request)
    return render(request, 'orders/view_order.html', context={'order': order})


# ---------------------------------------/ Item /-----------------------------------------------------

@login_required
def create_item(request):
    if request.user.is_admin_agent:
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if not form.is_valid():
                form = ItemForm(request.POST)
                messages.error(request, "Erro ao enviar formulario.")
                return render(request, 'orders/create_item.html', context={'form': form})
            form.save()
            messages.success(request, f'Item {request.POST.get("verbose_name")} criado com sucesso.')
        form = ItemForm()
        return render(request, 'orders/create_item.html', context={'form': form})
    else:
        messages.info(request, 'Você não tem acesso à esse recurso.')
        return render(request, 'utils/access_denied.html')


@login_required
def edit_items(request):
    if request.user.is_admin_agent:
        items = facade.get_all_items_by_category()
        if request.method == 'POST':
            if "":
                messages.error(request, "Erro ao enviar formulario.")
            # imagem = request.POST.get('imagem')
            messages.success(request, 'Formulário editado com sucesso.')
            return render(request, 'orders/edit_items.html', context={'categories': items, })

        return render(request, 'orders/edit_items.html', context={'categories': items, })
    else:
        messages.info(request, 'Você não tem acesso à esse recurso.')
        return render(request, 'utils/access_denied.html')


# ---------------------------/ Category /-------------------------------------


def create_category(request):
    return render(request, 'orders/create_category.html', context={'arg': "arg", })


def edit_category(request):
    return render(request, 'orders/edit_category.html', context={'arg': "arg", })


# -----------------------------/ Price Table /----------------------------------


@login_required
def create_price_table(request):
    return render(request, 'orders/create_price_table.html', context={'arg': "arg", })


@login_required
def edit_price_table(request):
    return render(request, 'orders/edit_price_table.html', context={'arg': "arg", })

