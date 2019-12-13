from django.urls import path
from .views import *

urlpatterns = [
    path('user_list/',UserList.as_view(),name="user_list"),
    path('user_add/',UserAddView.as_view(),name="user_add"),
    path('user_update/',UserUpdate.as_view(),name="user_update"),
    path('user_pms/',UserPermissions.as_view(),name="user_pms"),
    # path('testdata/',TestDataView.as_view()),


]


