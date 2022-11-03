from django.shortcuts import render

"""Главная страница"""


def index_page(request):
    return render(request, 'index.html')
