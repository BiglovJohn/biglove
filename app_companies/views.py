from django.shortcuts import render
from django.views import View
from pytils.translit import slugify
from .forms import CompanyProfileForm
from .models import CompanyProfile
from app_profiler.models import CustomUser

from app_premises.forms import RealtyObjectForm

"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ---"""


class CompanyEditFromView(View):
    def get(self, request, company_id):
        current_company = CompanyProfile.objects.get(user=company_id)
        company_id = current_company.id
        company_form = CompanyProfileForm(instance=current_company)
        realty_form = RealtyObjectForm()

        return render(request, 'app_companies/edit_company.html',
                      context={
                          'company_form': company_form,
                          'company_id': company_id,
                          'current_company': current_company,
                          'realty_form': realty_form,
                      }
                      )

    def post(self, request, company_id):
        current_company = CompanyProfile.objects.get(user=company_id)
        company_id = current_company.id
        company_form = CompanyProfileForm(request.POST, instance=current_company)
        realty_form = RealtyObjectForm(request.POST)

        if 'account__save_form' in request.POST and company_form.is_valid():
            company = company_form.save(commit=False)
            company.save()

        if 'account__save_realty_object' in request.POST and realty_form.is_valid():
            print('ФОРМА ВАЛИДНА')
            realty = realty_form.save(commit=False)
            realty.company = realty_form.cleaned_data['company']
            realty.slug = slugify(realty_form.cleaned_data['realty_name'])
            realty.realty_book_count = 0
            realty.save()
            realty_form.save_m2m()
            # for photo in files:
            #     Photos.objects.create(realty_obj=realty.id, photo=photo)

        return render(request, 'app_companies/edit_company.html',
                      context={
                          'company_form': company_form,
                          'company_id': company_id,
                          'current_company': current_company,
                          'realty_form': realty_form,
                      }
                      )


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""
