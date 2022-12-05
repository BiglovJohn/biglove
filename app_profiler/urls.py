from django.conf import settings
from django.urls import path
from .views import AnotherLogoutView, AccountEditFromView, AccountReservationListView, CompanyEditFromView, \
    register_step1, register_step2, register_step3
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_profiler'

urlpatterns = [
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('account/<slug:slug>/', AccountEditFromView.as_view(), name='account_detail'),
    path('account/<slug:slug>/reserve', AccountReservationListView.as_view(), name='account_reserves'),
    path('company/<int:company_id>/', CompanyEditFromView.as_view(), name='company_detail'),
    #  Шаги регистрации
    path('register/1', register_step1, name='register1'),
    path('register/2', register_step2, name='register2'),
    path('register/3', register_step3, name='register3'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
