"""
  Schema:
    A) Classes models inside the models.py
        Profession, DataSheet, Customer, Document
    B) Classes serializers inside the serializers.py
        CustomerSerializer, ProfessionSerializer
    C) Classes ViewSet inside the views.py
        CustomerViewSet, ProfessionViewSet
    D) Set the EndPoints inside the file urls.py
        router.register(r'customers', CustomerViewSet)
        router.register(r,'professions', ProfessionViewSet)
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import CustomerViewSet
from core.views import ProfessionViewSet
from core.views import DataSheetViewSet
from core.views import DocumentViewSet


router = routers.DefaultRouter()
# When override the get_queryset base_name is mandatory.
router.register(r'customers', CustomerViewSet, base_name="customer")
router.register(r'professions', ProfessionViewSet)
router.register(r'data-sheet', DataSheetViewSet)
router.register(r'documents', DocumentViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
