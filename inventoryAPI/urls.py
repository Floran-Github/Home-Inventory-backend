from django.urls import path
from .views import *

urlpatterns = [
    path('',InventoryAPI.as_view()),
    path('<int:pk>',InventoryProductAPI.as_view()),
]