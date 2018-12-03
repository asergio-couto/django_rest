"""
Serializers define the API representation
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
from rest_framework import serializers
from .models import Customer
from .models import Profession
from .models import DataSheet
from .models import Document


class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ('id', 'name', 'address', 'professions', 'data_sheet', 'active')


class ProfessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profession
    fields = ('id', 'description')


class DataSheetSerializer(serializers.ModelSerializer):
  class Meta:
    model = DataSheet
    fields = ( 'id', 'description', 'historical_data')


class DocumentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Document
    fields = ('id', 'dtype', 'doc_number', 'customer')
