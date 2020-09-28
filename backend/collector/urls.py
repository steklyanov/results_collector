from django.urls import path
from .views import ListCatchesView, CatchHandler

urlpatterns = [
    path('catch_handler/', CatchHandler.as_view()),
    path('catches_list/', ListCatchesView.as_view())
]