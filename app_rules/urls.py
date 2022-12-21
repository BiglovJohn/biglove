from django.conf import settings
from django.urls import path
from .views import our_values_page, rules_page, privacy_policy_page
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_rules'

urlpatterns = [
    path('values', our_values_page, name='our_values'),
    path('regulations', rules_page, name='rules'),
    path('privacy', privacy_policy_page, name='privacy_policy'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
