from django.urls import path
from .views import ListCatchesView, CatchHandler, PersonListView, SinglePersonView, GetLastImage

urlpatterns = [
    path('catch_handler/', CatchHandler.as_view()),
    path('catches_list/', ListCatchesView.as_view()),

    path('person_list/', PersonListView.as_view()),
    path('person/<int:id>/', SinglePersonView.as_view()),

    #     Получаю последний обьект catch из БД
    path('last_photo/', GetLastImage.as_view()),
]
