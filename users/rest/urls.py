from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = format_suffix_patterns([
    path('<int:pk>', views.UserProfileView.as_view()),
    path('<int:pk>/musts', views.MustsViewSet.as_view({'get': 'list'})),
    path('<int:pk>/musts/<int:game_id>', views.MustsViewSet.as_view({'delete': 'destroy', 'post': 'create'})),
])
