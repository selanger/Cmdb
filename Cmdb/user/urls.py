from django.urls import path
from .views import *

urlpatterns = [
    path('user_list/', UserList.as_view(), name="user_list"),
    path('user_add/', UserAddView.as_view(), name="user_add"),
    path('user_update/', UserUpdate.as_view(), name="user_update"),
    path('user_pms/', UserPermissions.as_view(), name="user_pms"),
    path('com_list/', CompanyList.as_view(), name="com_list"),
    path('com_add/', CompanyAddView.as_view(), name="com_add"),
    path('com_del/', CompanyDeleteView.as_view(), name="com_del"),
    # path('testdata/',TestDataView.as_view()),

]
