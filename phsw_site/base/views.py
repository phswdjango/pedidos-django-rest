from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


# ---------------/ User


@login_required
def create_user(request):
    return render(request, 'user/create_user.html', context={'arg': "arg", })


@login_required
def edit_user(request):
    return render(request, 'user/edit_user.html', context={'arg': "arg", })


# ---------------/ Company

@login_required
def create_company(request):
    return render(request, 'user/create_company.html', context={'arg': "arg", })


@login_required
def edit_company(request):
    return render(request, 'user/edit_company.html', context={'arg': "arg", })
