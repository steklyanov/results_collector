from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import Polygon
from .serializers import PolygonSerializer, SavePolygonSerializer

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as ShPolygon


def get_polygons(camera_id: int) -> list:
    """
    Input value: camera_id
    Output value: [ [shapely Polygon instance, Polygon Django model instance], [], ..., [] ]
    """
    polygons = Polygon.objects.filter(camera__id=camera_id).prefetch_related('point')
    polygon_array = []
    for polygon in polygons:
        points = polygon.point.all()
        single_polygon = ShPolygon([(point.x, point.y) for point in points])
        polygon_array.append([single_polygon, polygon])
    print("Create polygons", polygon_array)
    return polygon_array


def point_contains(x, y, polygons: list):
    """
    Input value: camera_id
    Output value: [ Bool, Model instance ]
    """
    point = Point(x, y)
    for polygon in polygons:
        if polygon[0].contains(point):
            return True, polygon[1]
    return False, polygon[1]


# Create your views here.
class AgentHandlerAPIView(APIView):
    def post(self, request):
        print("receive post")
        print(request.data)
        polygons = get_polygons(request.data["camera_id"])
        for i in range(len(request.data["data"]["dri"])):
            is_contain, polygon_instance = point_contains(request.data["data"]["dri"][i]["zone"]["x"],
                                                          request.data["data"]["dri"][i]["zone"]["y"], polygons)
            if not is_contain:
                print("Cached by polygon, continue")
                continue
            print("creating catch")


class CreatePolygonView(ListCreateAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer


class UpdatePolygonView(APIView):
    def post(self, request):
        serializer = SavePolygonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        print(serializer.errors)
        return Response(status=201)
