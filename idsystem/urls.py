# idsystem/idsystem/urls.py
from django.contrib import admin
from django.urls import include, path
from .routing import router
from Auth.views import generate_id_card  
from .docs import schema_view  
from django.views.generic import TemplateView

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('id-card/<str:user_id>/', generate_id_card, name='generate_id_card'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth-page/', TemplateView.as_view(template_name='index.html'), name='auth_page'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
