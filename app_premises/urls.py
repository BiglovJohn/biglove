from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from .views import main_realty_list, RealtyDetailView, ReservationFormView, RealtyEditFromView, permission_denied, \
    HolidayHouseObjectFormView, favorite, add_comment

app_name = 'app_premises'

urlpatterns = [
    path('', main_realty_list, name='realty_list'),
    path('russia/<slug:slug>/', RealtyDetailView.as_view(), name='realty_detail'),
    path('reservation', ReservationFormView.as_view(), name='reservation'),
    path('russia/<slug:slug>/edit', RealtyEditFromView.as_view(), name='realty_edit'),
    path('create/', HolidayHouseObjectFormView.as_view(), name='realty_create'),
    path('error/403', permission_denied, name='403'),
    re_path(r'^favorite/$', favorite, name='favorite'),
    re_path(r'^add_comment/$', add_comment, name='add_comment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
