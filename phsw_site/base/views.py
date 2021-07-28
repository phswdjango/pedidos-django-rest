from django.shortcuts import render, redirect


def home(request):
    # response = redirect('/usuario/login/')
    # return response
    return render(request, 'base/home.html')
