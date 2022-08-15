from django.urls import path, include
from rest_framework import routers
from .views import ParserView

app_name = 'API'

urlpatterns = [
    path('parse/', ParserView.as_view()),

]

