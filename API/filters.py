from django_filters import rest_framework as filters
from .models import Bill, Client


# choices = list(map(lambda x: (x.id, x.name), Client.objects.all()))

class BillFilter(filters.FilterSet):
    company__client = filters.ModelChoiceFilter(queryset=Client.objects.all(), label='Клиенты')

    class Meta:
        model = Bill
        fields = ['company', 'company__client']
