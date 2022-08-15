import django_filters
import pandas
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from .models import Client, Company, Pill
from .serializers import ClientSerializer, ParserSerializer, CompanySerializer, PillSerializer
from .filters import PillFilter
from .paginators import PillsPagination


class ParserView(APIView):

    def get(self, request):
        companies = Company.objects.all()
        clients = Client.objects.all()
        pills = Pill.objects.all()

        pars_data = pandas.read_excel('bills.xlsx', sheet_name='Лист1').values

        # кэши позволяют снизить количество запросов к БД
        cash_clients = {}
        cash_companys = {}

        for row in pars_data:
            client_name = row[0]
            company_name = row[1]
            internal_number = row[2]
            if len(row) < 6:  # пропускаем строки с неполными данными
                continue

            """обрабатываем данные КЛИЕНТА и сохраняем если валидны"""
            client_data = {
                'name': client_name,
            }

            client_serializer = ClientSerializer(data=client_data)

            if client_serializer.is_valid():
                if not clients.filter(name=client_name).exists():
                    client_serializer.save()
            if not cash_clients.get(client_name, None):  # если в кэше нет ключа с именем Клиента:
                client_id = Client.objects.get(name=client_name).id  # берем ID из БД
                cash_clients[client_name] = client_id  # записываем в кэш

            """обрабатываем данные КОМПАНИИ и сохраняем если валидны"""
            company_data = {
                'name': company_name,
                'client': cash_clients[client_name]
            }
            company_serializer = CompanySerializer(data=company_data)

            if company_serializer.is_valid():
                if not companies.filter(name=company_name).exists():
                    company_serializer.save()
            if not cash_companys.get(company_name, None):  # если в кэше нет ключа с именем компании:
                company_id = Company.objects.get(name=company_name).id  # берем ID из БД
                cash_companys[company_name] = company_id  # записываем в кэш

            """обрабатываем данные Счетов и сохраняем если валидны"""
            pill_data = {
                'company': cash_companys[company_name],
                'internal_number': row[2],
                'summ': row[3],
                'date': row[4].strftime("%Y-%m-%d"),
                'service': row[5],
            }

            pill_serializer = ParserSerializer(data=pill_data)

            if pill_serializer.is_valid():
                # у каждой компании номер счета уникален
                pill = pills.filter(Q(internal_number=internal_number) & Q(company=cash_companys[company_name]))
                # если в БД нет такого счета то записываем его
                if not pill.exists():
                    pill_serializer.save()

        return Response('данные обновлены')


class PillView(viewsets.ModelViewSet):
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PillFilter
    pagination_class = PillsPagination