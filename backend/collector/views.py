from .models import Catch, Person
from .serializers import CatchSerializer, PersonSerializer

from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import names
import base64
import time


class CatchHandler(APIView):
    def post(self, request):
        print("RECEIVE POST")
        if "ex_id" and "image" in request.data:
            person, _ = Person.objects.get_or_create(ex_id=request.data["ex_id"],
                                                     defaults={'name': names.get_full_name()})
            image_string = request.data["image"]
            Catch.objects.create(person=person,
                                 image=ContentFile(base64.b64decode(image_string),
                                                   name=str(request.data["ex_id"]) +
                                                        time.strftime("%Y%m%d-%H%M%S") + '.jpg'))

            return Response(status=status.HTTP_201_CREATED)
        else:
            Response({"error": "no external id or image provided"}, status=status.HTTP_204_NO_CONTENT)


class ListCatchesView(generics.ListAPIView):
    queryset = Catch.objects.all()
    serializer_class = CatchSerializer
