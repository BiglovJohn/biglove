from django.conf import settings
from django.urls import path
from .views import our_values_page
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_rules'

urlpatterns = [
    path('values/', our_values_page, name='our_values'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
