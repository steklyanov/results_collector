from django.urls import path
from .views import CreatePolygonView, UpdatePolygonView, GetCameraView

urlpatterns = [
    path('create/', CreatePolygonView.as_view()),
    path('update/', UpdatePolygonView.as_view()),

    path('get_camera/<cam_id>/', GetCameraView.as_view())

]
