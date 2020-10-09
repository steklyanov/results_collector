from django.contrib import admin
from .models import Camera, Polygon, PolygonPoint

admin.site.register(Camera)
admin.site.register(Polygon)
admin.site.register(PolygonPoint)
