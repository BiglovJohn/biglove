from .models import LocationModel


def render_location_info(request):
    countries = LocationModel.objects.order_by().values('country').distinct()
    regions = LocationModel.objects.order_by().values('region').distinct()
    districts = LocationModel.objects.order_by().values('district').distinct()
    cities = LocationModel.objects.order_by().values('city').distinct()
    return {'countries': countries, 'regions': regions, 'districts': districts, 'cities': cities, }
