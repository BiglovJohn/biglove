from app_premises.models import RealtyOptions, TechniqueModel, FurnitureModel


IN_HOTEL_OPTIONS = list(RealtyOptions.objects.values_list('id', 'option_name').filter(category='На территории'))
IN_ROOM_OPTIONS = list(RealtyOptions.objects.values_list('id', 'option_name').filter(category='В номере'))

FURNITURE = list(FurnitureModel.objects.values_list('id', 'name'))
TECHNIQUE = list(TechniqueModel.objects.values_list('id', 'name'))
