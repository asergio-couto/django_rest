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

Queryset
  Para recuperar objetos do seu banco de dados, construa uma QuerySet através
  da Manager na sua classe de modelo.
  A QuerySet representa uma coleção de objetos do seu banco de dados. Ele pode
  ter zero, um ou muitos filtros.
  Filtros limitam os resultados baseado nos parâmetros dados.
  Em termos de SQL, um QuerySet equivale a um comando SELECT, e um filtro é uma
  clásula limitante tal como WHERE or LIMIT.
  Você chega a um QuerySet usando o Manager do modelo.
  Cada mdoelo tem no mínimo um Manager, e é por padrão chamado objects.
  Acesse ele diretamente através da classe do modelo.

"""
from rest_framework import viewsets
from rest_framework.response import Response

# from django.http.response import HttpResponseNotAllowed, HttpResponseForbidden
from rest_framework.decorators import action

from core.serializers import CustomerSerializer
from core.serializers import ProfessionSerializer
from core.serializers import DataSheetSerializer
from core.serializers import DocumentSerializer

from .models import Customer
from .models import Profession
from .models import DataSheet
from .models import Document

class CustomerViewSet(viewsets.ModelViewSet):
  # queryset = Customer.objects.all()
  serializer_class = CustomerSerializer

  # TODO: 18.Query string
  # Override get_queryset
  def get_queryset(self):
    id = self.request.query_params.get('id', None)
    # Queryset por Id and active
    status = True if self.request.query_params['active'] == 'True' else False

    if id:
      customers = Customer.objects.filter(id=id, active=status)
    else:
      customers = Customer.objects.filter(active=status)
    return customers

  # Overrinding the behaviour of the list method
  def list(self, request, *args, **kwargs):
    customers = self.get_queryset()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

  # Overriding Retrieve method
  # **kwargs: Customer.objects.get(id=kwargs['pk'])
  def retrieve(self, request, *args, **kwargs):
    customer = self.get_object()
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

    # return HttpResponseNotAllowed('Not allowed')
    # return HttpResponseForbidden('Not allowed')

  # Overriding the behavior of the POST method
  def create(self, request, *args, **kwargs):
    data = request.data
    customer = Customer.objects.create(
      name=data['name'],
      address=data['address'],
      # Relationship OneToOne
      data_sheet_id=data['data_sheet'],
    )
    # Relationship ManyToMany
    profession = Profession.objects.get(id=data['profession'])

    customer.professions.add(profession)
    customer.save()

    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

  # Overriding the behavior of the PUT method
  def update(self, request, *args, **kwargs):
    customer = self.get_object()
    data = request.data
    customer.name = data['name']
    customer.address = data['address']
    # Relationship OneToOne
    customer.data_sheet_id = data['data_sheet']
    # Relationship ManyToMany
    profession = Profession.objects.get(id=data['profession'])

    for p in customer.professions.all():
      customer.professions.remove(p)

    customer.professions.add(profession)
    customer.save()

    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

  # Overriding the behavior of the PATCH method for partial Update
  def partial_update(self, request, *args, **kwargs):
    customer = self.get_object()
    customer.name = request.data.get('name', customer.name)
    customer.address = request.data.get('address', customer.address)
    customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)

    customer.save()
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

  # 16.Overriding the behavior of the DELETE method
  def destroy(self, request, *args, **kwargs):
    customer = self.get_object()
    customer.delete()

    return Response('Object removed')

  # 17.Create Custom actions
  # Conforme o para na url este action ativa ou desativa o registro
  # http://localhost:8000/api/customers/5/deactivate/
  # http://localhost:8000/api/customers/5/activate
  @action(detail=True)
  def deactivate(self, request, **kwargs):
    customer = self.get_object()
    customer.active = False
    customer.save()
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

  @action(detail=False)
  def deactivate_all(self, request, **kwargs):
    customers = self.get_queryset()
    customers.update(active=False)

    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

  @action(detail=False)
  def activate_all(self, request, **kwargs):
    customers = self.get_queryset()
    customers.update(active=True)

    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

  @action(detail=False, methods=['POST'])
  def change_status(self, request, **kwargs):
    status = True if request.data['active'] == 'True' else False

    customers = self.get_queryset()
    customers.update(active=status)

    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


#########################################################################


class ProfessionViewSet(viewsets.ModelViewSet):
  # query = Profession.objects.filter()
  queryset = Profession.objects.all()
  serializer_class = ProfessionSerializer


#########################################################################


class DataSheetViewSet(viewsets.ModelViewSet):
  queryset = DataSheet.objects.all()
  serializer_class = DataSheetSerializer


#########################################################################


class DocumentViewSet(viewsets.ModelViewSet):
  queryset = Document.objects.all()
  serializer_class = DocumentSerializer
