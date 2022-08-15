from django.urls import path, include
from rest_framework import routers
from .views import ParserView, PillView
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'pills', PillView)


app_name = 'API'

urlpatterns = [
    path('parse/', ParserView.as_view()),
    path('', include(router.urls))
]

urlpatterns += doc_urls