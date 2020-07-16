"""foodtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings             # add this
from django.conf.urls.static import static
from .views import serve_frontend_view
from authentication.urls import urlpatterns as authentication_url_patterns
from core.urls import urlpatterns as core_url_patterns
from mailing.urls import urlpatterns as mailing_url_patterns
from django.views.generic import RedirectView, TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/authentication/', include(authentication_url_patterns, namespace='authentication')),
    url(r'^api/core/', include(core_url_patterns)),
    url(r'^api/mailing/', include(mailing_url_patterns)),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

]

# add this
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
