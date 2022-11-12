from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import auto_index_page
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'app_auto'

urlpatterns = [
    path('', auto_index_page, name='auto_index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()