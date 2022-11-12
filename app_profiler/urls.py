from django.conf import settings
from django.urls import path
from .views import AnotherLogoutView, AccountEditFromView, AccountReservationListView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_profiler'

urlpatterns = [
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('<slug:slug>/', AccountEditFromView.as_view(), name='account_detail'),
    path('<slug:slug>/reserve', AccountReservationListView.as_view(), name='account_reserves'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
