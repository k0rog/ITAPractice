from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.GamesListView.as_view(), name='games'),
    path('<slug:slug>', views.GameDetailView.as_view(), name='detail_page'),
]
