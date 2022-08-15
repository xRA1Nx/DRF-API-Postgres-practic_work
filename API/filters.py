from django_filters import rest_framework as filters
from .models import Pill, Client

choices = list(map(lambda x: (x.id, x.name), Client.objects.all()))


class PillFilter(filters.FilterSet):

    company__client = filters.ChoiceFilter(choices=choices, label="client")

    class Meta:
        model = Pill
        fields = ['company', 'company__client']
