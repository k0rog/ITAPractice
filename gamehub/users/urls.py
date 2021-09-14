from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('registration', views.SignUpView.as_view(), name='registration'),
    path('authorization', views.SignInView.as_view(), name='authorization'),
    path('logout', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('profile', views.UserProfileView.as_view(), name='profile_page'),
    path('my_musts', views.UserMustsView.as_view(), name='musts'),
    path('musts', views.MustsView.as_view(), name='musts_update')
]
