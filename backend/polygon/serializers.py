from rest_framework import serializers
from .models import Camera, Polygon, PolygonPoint


class SavePolygonSerializer(serializers.Serializer):
    camera_id = serializers.CharField()
    polygons = serializers.ListField()

    def create(self, validated_data):
        polygons = validated_data.pop('polygons')
        camera = Camera.objects.get(id=validated_data["camera_id"])
        current_polygons = Polygon.objects.filter(camera=camera)
        [polygon.delete() for polygon in current_polygons]
        new_polygon = None

        for polygon in polygons:
            print(polygon)
            new_polygon = Polygon.objects.create(camera=camera, type=polygon["type"])
            [PolygonPoint.objects.create(polygon=new_polygon, **point) for point in polygon["polygon"]]
        if new_polygon is None:
            new_polygon = Polygon.objects.create(camera=camera, type="0")
        return new_polygon


class PolygonPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonPoint
        fields = ['x', 'y', 'id']


class PolygonSerializer(serializers.ModelSerializer):
    point = PolygonPointSerializer(read_only=True, many=True)

    class Meta:
        model = Polygon
        fields = ['point', 'id', 'type']


class CameraSerializer(serializers.ModelSerializer):
    polygon = PolygonSerializer(read_only=True, many=True)

    class Meta:
        model = Camera
        fields = '__all__'
