from django.urls import path
from applications.account.views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view())
]