"""Routes racine du projet ``acronyme``.

Compose deux groupes de routes :

- les routes applicatives, incluses depuis :mod:`acronyme.urls`,
- les routes de documentation OpenAPI/Swagger fournies par
  ``drf-spectacular`` :

  - ``/swagger/`` — Swagger UI,
  - ``/swagger/schema/`` — schéma OpenAPI brut,
  - ``/swagger/redoc/`` — Redoc.
"""

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', include('acronyme.urls')),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
