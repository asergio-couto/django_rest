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
from django.db import models


class Profession(models.Model):
  description = models.CharField(max_length=50)

  def __str__(self):
    return self.description


class DataSheet(models.Model):
  description = models.CharField(max_length=50)
  historical_data = models.TextField()

  def __str__(self):
    return self.description


class Customer(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=50)
  active = models.BooleanField(default=True)
  doc_num = models.CharField(max_length=12, unique=True, null=True, blank=True)
  professions = models.ManyToManyField(Profession)
  data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.name


class Document(models.Model):
  PP = 'pp'
  ID = 'ID'
  OT = 'OT'

  DOC_TYPES = ((PP, 'Passaport'), (ID, 'Identity card'), (OT, 'Others'))

  dtype = models.CharField(choices=DOC_TYPES, max_length=2)
  doc_number = models.CharField(max_length=50)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

  def __str__(self):
    return self.doc_number
