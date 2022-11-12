from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index_page
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'app_index'

urlpatterns = [
    path('', index_page, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()