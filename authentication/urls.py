from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from .views import UserView,activate, LoginView,RegistrationView# LogoutView,
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

# router = routers.DefaultRouter()
# # router.register(r'user', UserView.as_view(), basename="user")
# router.register(r'login/?$'', LoginView.as_view(), basename="login")
# # router.register(r'user/logout', LogoutViewSet)
# router.register(r'register', RegistrationView.as_view(), basename="register")

urlpatterns = ([
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    # url(r'^social/(?P<backend>[^/]+)/$', exchange_token),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate')
    # url(r'^', include(router.urls)),
], 'authentication')