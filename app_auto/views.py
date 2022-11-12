from django.shortcuts import render

from app_companies.models import CompanyProfile

"""Главная страница"""


def auto_index_page(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            user_slug = request.user.slug
            current_company = CompanyProfile.objects.get(user=request.user.id)
            company_slug = current_company.slug
            return render(request, 'app_auto/auto_index.html', {'user_slug': user_slug, 'company_slug': company_slug})
        else:
            user_slug = request.user.slug
            company_slug = None
            return render(request, 'app_auto/auto_index.html', {'user_slug': user_slug, 'company_slug': company_slug})
    else:
        user_slug = None
        company_slug = None
        return render(request, 'app_auto/auto_index.html', {'user_slug': user_slug, 'company_slug': company_slug})
