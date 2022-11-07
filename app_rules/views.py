from django.shortcuts import render


def our_values_page(request):
    return render(request, 'app_rules/our_values.html')
