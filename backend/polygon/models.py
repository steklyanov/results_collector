from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=500)


class Polygon(models.Model):
    POLYGON_TYPES = (
        ("0", "Вьезд"),
        ("1", "Выезд"),
        ("2", "Мусор")
    )

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='polygon', null=True, blank=True)
    type = models.CharField(max_length=6, verbose_name='Тип полигона', choices=POLYGON_TYPES)


class PolygonPoint(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, related_name='point', null=True, blank=True)
