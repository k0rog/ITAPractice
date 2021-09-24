from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.GameViewSet.as_view({'get': 'list'})),
    path('<int:pk>', views.GameViewSet.as_view({'get': 'retrieve'})),
])
