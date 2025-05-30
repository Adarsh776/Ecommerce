"""
URL configuration for ecommmerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from authentication import views as authview
from coreapp import views as coreview


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',coreview.Openpage.as_view(),name='openpage'),
    path('authentication/',include('authentication.urls')),
    path('coreapp/',include('coreapp.urls')),
    path('orderapp/',include('orderapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('cartapp/',include('cartapp.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)