"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    #path('login/', views.login, name='login'),
    path('login/',
         LoginView.as_view(template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }),
         name='login'),
    path('admin/', admin.site.urls),
    path('accounts/login/', 
         LoginView.as_view(template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }),
         name='login'),
    path('organizations/', views.organizations, name='organizations'),
    path('addOrganization/', views.addOrganization, name='addOrganization'),
    path('shareUnShareOrganization/', views.shareUnShareOrganization, name='shareUnShareOrganization'),
    path('devices/', views.devices, name='devices'),
    path('addDevice/', views.addDevice, name='addDevice'),
    path('on/', views.on, name='on'),
    path('off/', views.off, name='off'),
    path('attach/', views.attach, name='attach'),
    path('detach/', views.detach, name='detach'),
    path('notifications/', views.notifications, name='notifications'),
    path('catalog', views.catalog, name='catalog'),
    path('parts', views.parts, name='parts'),
    path('addPart', views.addPart, name='addPart'),
    path('addDeviceToCatalog', views.addDeviceToCatalog, name='addDeviceToCatalog'),
    path('removePart/', views.removePart, name='removePart'),
    path('loginCheck/', views.loginCheck, name='loginCheck'),
    path('lobby/', views.lobby, name='lobby'),
    path('setNotificationTime/', views.setNotificationTime , name='setNotificationTime'),
    ]