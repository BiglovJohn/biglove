from django.conf import settings
from django.urls import path
from .views import AnotherLogoutView, AccountEditFromView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'app_profiler'

urlpatterns = [
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('<int:user_id>/', AccountEditFromView.as_view(), name='account_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()