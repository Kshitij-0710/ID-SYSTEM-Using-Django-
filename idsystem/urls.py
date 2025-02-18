from django.contrib import admin
from django.urls import include, path
from .routing import router  # Your DRF API routes
from .docs import schema_view  # Your OpenAPI schema

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include your API endpoints

    # Swagger UI:
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc UI:
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
