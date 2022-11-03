from django.conf import settings
from django.urls import path
from .views import CompanyEditFromView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_companies'

urlpatterns = [
    path('<int:company_id>/', CompanyEditFromView.as_view(), name='company_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
