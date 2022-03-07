from django.contrib import admin
from django.urls import path, include

# require the built-in class-based views from simpleJWT to utilize in our auth api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/token/', TokenObtainPairView.as_view()), # used to login
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('auth/user/', include('user.urls')),
]
