from .models import CompanyProfile


def render_current_company_slug(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            current_company = CompanyProfile.objects.get(user=request.user.id)
            company_slug = current_company.slug
            return {'company_slug': company_slug}
        else:
            company_slug = None
            return {'company_slug': company_slug}
    else:
        company_slug = None
        return {'company_slug': company_slug}