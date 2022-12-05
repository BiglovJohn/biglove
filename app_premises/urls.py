from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from .views import main_realty_list, RealtyDetailView, ReservationFormView, RealtyEditFromView, permission_denied, \
    HolidayHouseObjectFormView, favorite, add_comment, main_lt_realty_list, LongTermRealtyDetailView, \
    LonTermRealtyEditFromView, LongTermObjectFormView, lt_favorite, RegisterObject, create_camp_object_step1, \
    create_camp_object_step2, create_camp_object_step3, create_camp_object_step4, create_camp_object_step5, \
    create_camp_object_step6, create_camp_object_step7, create_camp_object_step8

app_name = 'app_premises'

urlpatterns = [
    path('', main_realty_list, name='realty_list'),
    path('russia/<slug:slug>/', RealtyDetailView.as_view(), name='realty_detail'),
    path('reservation', ReservationFormView.as_view(), name='reservation'),
    path('russia/<slug:slug>/edit', RealtyEditFromView.as_view(), name='realty_edit'),

    path('create-camp/1', create_camp_object_step1, name='create_camp1'),
    path('create-camp/2', create_camp_object_step2, name='create_camp2'),
    path('create-camp/3', create_camp_object_step3, name='create_camp3'),
    path('create-camp/4', create_camp_object_step4, name='create_camp4'),
    path('create-camp/5', create_camp_object_step5, name='create_camp5'),
    path('create-camp/6', create_camp_object_step6, name='create_camp6'),
    path('create-camp/7', create_camp_object_step7, name='create_camp7'),
    path('create-camp/8', create_camp_object_step8, name='create_camp8'),

    path('error/403', permission_denied, name='403'),
    path('long/', main_lt_realty_list, name='lt_realty_list'),
    path('<int:pk>/', LongTermRealtyDetailView.as_view(), name='lt_realty_detail'),
    path('<int:pk>/edit', LonTermRealtyEditFromView.as_view(), name='lt_realty_edit'),
    path('create-long-term/', LongTermObjectFormView.as_view(), name='lt_realty_create'),
    path('register-object/', RegisterObject.as_view(), name='register_object'),

    re_path(r'^favorite/$', favorite, name='favorite'),
    re_path(r'^add_comment/$', add_comment, name='add_comment'),
    re_path(r'^lt_favorite/$', lt_favorite, name='lt_favorite'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
