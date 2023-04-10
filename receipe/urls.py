from django.urls import path
from .views import *


urlpatterns = [
    path("list/<int:pk>",ReceipeSuggestionListAPI.as_view()),
    path("detail",ReceipeSuggestionAPi.as_view()),
]