from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from phsw_site.base.api.views import (
    registration_view, check_user_view,
)

app_name = 'base'
urlpatterns = [
    path('register', registration_view, name='register'),
    path('check_user/<slug>/', check_user_view, name='check_user'),
    path('login', obtain_auth_token, name='login'),
]
