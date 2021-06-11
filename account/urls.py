from django.contrib import admin
from django.urls import path

from .views.account import ApiLoginView,ObtainAccount

urlpatterns = [
    path('login/', ApiLoginView.as_view(), name='login'),
    path('logout/', ObtainAccount.as_view({'post': 'logout'}), name='logout'),
    path('register/', ObtainAccount.as_view({'post': 'register'}), name='register'),
    path('activate/<uidb64>/<token>/', ObtainAccount.as_view({'get': 'activate'}), name='activate'),
    # path('home/', ObtainAccount.as_view({'post': 'home'})),
    # path('token/',ReceiverAccount.as_view({'post':'getToken'})),
    # path('token/accept/',ReceiverAccount.as_view({'post':'receiveToken'})),
]