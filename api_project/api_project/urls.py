from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title='API Documentation',
      default_version='v1',
      description="API for Educational Center",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('', lambda _: redirect('presentation')),
   path('admin/', admin.site.urls),
   path('api/prod/', include('api_product.urls')),
   path('api/auth/', include('api_authentication.urls')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='presentation'),
]
