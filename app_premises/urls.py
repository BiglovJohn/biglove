from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import main_realty_list, RealtyDetailView, ReservationFormView, RealtyEditFromView, permission_denied

app_name = 'app_premises'

urlpatterns = [
    path('russia', main_realty_list, name='realty_list'),
    path('<slug:slug>/', RealtyDetailView.as_view(), name='realty_detail'),
    path('reservation', ReservationFormView.as_view(), name='reservation'),
    path('<slug:slug>/edit', RealtyEditFromView.as_view(), name='realty_edit'),
    path('error/403', permission_denied, name='403')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
