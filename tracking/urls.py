from django.urls import path
from . import views

urlpatterns = [
    path("shipments_list/", views.shipments_list),
    path("shipment/", views.shipment),
]
