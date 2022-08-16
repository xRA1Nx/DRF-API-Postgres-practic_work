import os

import django_filters
import pandas
import glob
import random
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from .models import Client, Company, Bill, ServiceClass
from .serializers import ClientSerializer, ParserSerializer, CompanySerializer, BillSerializer
from .filters import BillFilter
from .paginators import BillsPagination


class ParserView(APIView):

    def get(self, request):

        # делаем запросы к бд для дальнейшей работы с данными
        companies = Company.objects.all()
        clients = Client.objects.all()
        bills = Bill.objects.all()
        service_classes = ServiceClass.objects.all()

        # кэши позволяют снизить количество запросов к БД
        cash_clients = {}
        cash_companys = {}

        # если 1-й раз парсим, то наполняем таблицу ServiceClass
        if not service_classes:
            ServiceClass.objects.create(name='консультация', code=1)
            ServiceClass.objects.create(name='лечение', code=2)
            ServiceClass.objects.create(name='стационар', code=3)
            ServiceClass.objects.create(name='диагностика', code=4)
            ServiceClass.objects.create(name='лаборатория', code=5)
            service_classes = ServiceClass.objects.all()

        for file in glob.glob('clients_bills/*.xlsx'):
            client_name = os.path.basename(file).split('_')[0]
            parser = pandas.read_excel(file, sheet_name='Лист1')
            pars_data = parser.values
            pars_colums = parser.columns
            company_ind = -100
            num_ind = -100
            summ_ind = -100
            date_ind = -100
            serv_ind = - 100

            # функция обработчик, проверяющаа есть ли слова keywords в названии поля
            def check_data(keywords: set, index: int) -> bool:
                for word in keywords:
                    if word in pars_colums[index].lower():
                        return True
                return False

            # получаем индексы столбцов исходя из их названия (столбцы могут располагаться в любом порядке)
            for i in range(len(pars_colums)):
                if check_data({'org', }, i):
                    company_ind = i
                if check_data({'№', 'number', }, i):
                    num_ind = i
                if check_data({'sum', 'total', }, i):
                    summ_ind = i
                if check_data({'created', 'date', }, i):
                    date_ind = i
                if check_data({'service', }, i):
                    serv_ind = i

            for row in pars_data:
                company_name = row[company_ind]
                internal_number = row[num_ind]
                summ = row[summ_ind]
                date_in = row[date_ind]
                service = row[serv_ind]

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
                bill_data = {
                    'company': cash_companys[company_name],
                    'internal_number': internal_number,
                    'summ': summ,
                    'date': date_in.strftime("%Y-%m-%d"),
                    'service': service,
                    'service_class': random.randrange(service_classes[0].id, service_classes[0].id + len(service_classes))
                }

                bill_serializer = ParserSerializer(data=bill_data)

                if bill_serializer.is_valid():
                    # у каждой компании номер счета уникален
                    bill = bills.filter(Q(internal_number=internal_number) & Q(company=cash_companys[company_name]))
                    # если в БД нет такого счета то записываем его
                    if not bill.exists():
                        bill_serializer.save()
                else:
                    print(bill_serializer.errors)

        return Response('данные обновлены')


class BillView(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = BillFilter
    pagination_class = BillsPagination
