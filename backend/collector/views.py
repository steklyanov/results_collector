from .models import Catch, Person
from .serializers import CatchSerializer, PersonSerializer

from django.core.files.base import ContentFile
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import names
import base64
import time


class CatchHandler(APIView):
    def post(self, request):
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
            return Response({"error": "no external id or image provided"}, status=status.HTTP_204_NO_CONTENT)


class ListCatchesView(generics.ListAPIView):
    serializer_class = CatchSerializer

    def get_queryset(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('''select person_id, array_agg(t2.*) as catch_groups from (select * from collector_catch
                        left join "collector_person"
                        on ("collector_catch"."person_id" = "collector_person"."id")
                        order by collector_catch.datetime, collector_catch.person_id asc ) t2 group by t2.person_id''')
        rows = cursor.fetchall()
        print(rows)
        print(self.request.query_params)
        print(args)
        print(kwargs)
        return rows
