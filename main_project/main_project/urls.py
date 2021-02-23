from django.contrib import admin
from django.urls import path, include

from mainapp import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
