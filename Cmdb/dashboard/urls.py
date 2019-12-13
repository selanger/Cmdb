from django.urls import path
from .views import *

urlpatterns = [
    path('index/',Index.as_view(),name="index"),
    path('login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
]


