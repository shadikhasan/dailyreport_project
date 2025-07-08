
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from dailyreport.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dailyreport.urls')),
    
    path('', dashboard_view, name='dashboard'),  # default home page
    
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]