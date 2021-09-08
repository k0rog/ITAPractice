from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('detail_page', views.detail_page, name='detail_page'),
]