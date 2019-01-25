from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from api.dispatcher import Dispatcher

urlpatterns = [
    path('driver/', views.DriverList.as_view()),
    path('driver/<int:pk>/', views.DriverDetail.as_view()),
    path('shipment/', views.ShipmentList.as_view()),
    path('shipment/<int:pk>/', views.ShipmentDetail.as_view()),
    path('dispatch/', views.DispatchList.as_view()),
    path('dispatch/<int:pk>/', views.DispatchDetail.as_view()),
    path('driver/<int:pk>/dispatch/$', Dispatcher.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
