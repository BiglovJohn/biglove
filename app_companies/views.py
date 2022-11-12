from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from pytils.translit import slugify
from .forms import CompanyProfileForm
from .models import CompanyProfile
from app_profiler.models import CustomUser
from app_premises.forms import HolidayHouseForm

"""---РАЗДЕЛ ВЬЮШЕК ПО ОБЪЕКТАМ ПРОФИЛЕЙ---"""


class CompanyEditFromView(View):
    def get(self, request, company_slug):
        current_company = CompanyProfile.objects.get(user=request.user.id)
        current_slug = current_company.slug
        if company_slug == current_slug:
            current_company = CompanyProfile.objects.get(slug=company_slug)
            if current_company.user.id == request.user.id:
                company_id = current_company.id
                company_form = CompanyProfileForm(instance=current_company)
                realty_form = HolidayHouseForm()
                return render(request, 'app_companies/edit_company.html',
                              context={
                                  'company_form': company_form,
                                  'company_id': company_id,
                                  'current_company': current_company,
                                  'realty_form': realty_form,
                                  'company_slug': company_slug,
                              }
                              )
            else:
                return redirect('app_companies:company_detail', company_slug=company_slug)
        else:
            current_company = CompanyProfile.objects.get(user=request.user.id)
            return redirect('app_companies:company_detail', company_slug=current_company.slug)

    def post(self, request, company_slug):
        current_company = CompanyProfile.objects.get(slug=company_slug)
        company_form = CompanyProfileForm(request.POST, instance=current_company)
        realty_form = HolidayHouseForm(request.POST)

        if 'account__save_form' in request.POST:
            if company_form.is_valid():
                company = company_form.save(commit=False)
                company.slug = company_form.cleaned_data['slug'].lower()
                company.save()
                return redirect('app_companies:company_detail', company_slug=company_slug)
            else:
                messages.error(request, 'Ошибка при изменении ссылки на компанию')
            return redirect('app_companies:account_detail', company_slug=company_slug)

        if 'account__save_realty_object' in request.POST and realty_form.is_valid():
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
                          'company_slug': company_slug,
                          'current_company': current_company,
                          'realty_form': realty_form,
                      }
                      )


"""---КОНЕЦ РАЗДЕЛА ВЬШЕК ПО ОБЪЕКТАМ НЕДВИЖИМОСТИ---"""
