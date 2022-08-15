import datetime
from rest_framework import serializers
from .models import Company, Client, Bill


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    def valadate_name(self, value):
        if value and value != '-':
            return value
        raise serializers.ValidationError("поле 'client' не заполнено или заполненно не корректно")

    class Meta:
        model = Client
        fields = "__all__"


class CompanyNestedSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Company
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    def valadate_company(self, value):
        if value and value != '-':
            return value
        raise serializers.ValidationError("поле 'company' не заполнено или заполненно не корректно")

    class Meta:
        model = Company
        fields = "__all__"


class ParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    company = CompanyNestedSerializer()

    def validate_summ(self, value):
        if type(value) in [float, int]:
            return value
        else:
            raise serializers.ValidationError("поле 'summ' д.б. числом")

    def validate_service(self, value):
        if value and value != '-':
            return value
        else:
            raise serializers.ValidationError("поле 'Serive' не заполнено или заполненно не корректно")

    def valadate_date(self, value):
        if type(value) == datetime.date:
            return value
        raise serializers.ValidationError("поле 'date' заполнено не корректно")

    def valadate_internal_number(self, value):
        if isinstance(value, int):
            return value
        raise serializers.ValidationError("поле 'internal_number' заполнено не корректно")

    class Meta:
        model = Bill
        fields = "__all__"
