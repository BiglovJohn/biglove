from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from .views import main_lt_realty_list, LongTermRealtyDetailView, LonTermRealtyEditFromView, LongTermObjectFormView,\
    lt_favorite

app_name = 'app_ltrent'

urlpatterns = [
    path('', main_lt_realty_list, name='lt_realty_list'),
    path('<int:pk>/', LongTermRealtyDetailView.as_view(), name='lt_realty_detail'),
    path('<int:pk>/edit', LonTermRealtyEditFromView.as_view(), name='lt_realty_edit'),
    path('create/', LongTermObjectFormView.as_view(), name='lt_realty_create'),
    re_path(r'^lt_favorite/$', lt_favorite, name='lt_favorite'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
