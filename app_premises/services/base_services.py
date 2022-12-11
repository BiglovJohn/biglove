from app_premises.models import RealtyOptions


IN_HOTEL_OPTIONS = list(RealtyOptions.objects.values_list('id', 'option_name').filter(category='В отеле'))
IN_ROOM_OPTIONS = list(RealtyOptions.objects.values_list('id', 'option_name').filter(category='В номере'))
