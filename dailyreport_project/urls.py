from django.contrib import admin
from django.urls import path, include
from dailyreport.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home-redirect'),  # <--- THIS IS THE KEY LINE!
    path('', include('dailyreport.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
]
