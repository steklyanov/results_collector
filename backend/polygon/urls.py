from django.urls import path
from .views import CreatePolygonView, UpdatePolygonView

urlpatterns = [
    path('create/', CreatePolygonView.as_view()),
    path('update/', UpdatePolygonView.as_view())

]
