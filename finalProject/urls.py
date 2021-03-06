"""finalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Organization API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('organization/', include('organization.urls')),
    path('products/', include('products.urls')),
    path('', auth_view.LoginView.as_view(), name='login'),
    path('sale/', include('sale.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwtauth/', include('jwtauth.urls'), name='jwt authentication'),
    path('api/docs/', schema_view)
]
