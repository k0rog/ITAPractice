from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register_user, name='registration'),
    path('authorization', views.authorize_user, name='authorization'),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.profile_page, name='profile_page'),
]
