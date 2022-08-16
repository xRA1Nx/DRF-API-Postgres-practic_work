from django.db import models


class Client(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(unique=True, max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bill(models.Model):
    date = models.DateField()
    summ = models.FloatField()
    internal_number = models.IntegerField()
    service = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        # unique_together = ('internal_number', 'company') - лучше не использовать, может устареть в будущем
        constraints = [
            models.UniqueConstraint(fields=['internal_number', 'company'], name='company_pill')
        ]


class ServiceClass(models.Model):
    name = models.CharField(max_length=20)
    code = models.IntegerField()
