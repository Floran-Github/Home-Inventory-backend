from django.urls import path
from .views import *


urlpatterns = [
    path('user/list',UserTransactionsListViewAPI.as_view()),
    path("detail/<int:pk>",UserTransactionsDetailViewAPI.as_view()),
]