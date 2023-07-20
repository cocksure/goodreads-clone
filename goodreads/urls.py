from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import LandingPage, home_page


urlpatterns = [
    path("", LandingPage.as_view(), name='landing_page'),
    path("home/", home_page, name='home_page'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api/', include('api.urls')),


    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
