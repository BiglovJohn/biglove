from django.shortcuts import render
from app_premises.models import Photos, Camp

"""Главная страница"""


def index_page(request):
    index_realty_list = Camp.objects.order_by('-realty_book_count')[:7]
    return render(request, 'index.html', {'index_realty_list': index_realty_list})
