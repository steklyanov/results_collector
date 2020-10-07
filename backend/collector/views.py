from .models import Catch, Person
from .serializers import NestedCatchesSerializer, CatchSerializer, PersonSerializer

from django.core.files.base import ContentFile
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import names
import base64
import time
import datetime


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
    serializer_class = NestedCatchesSerializer

    def get_queryset(self, *args, **kwargs):
        cursor = connection.cursor()
        from_datetime = self.request.query_params.get("from", datetime.datetime.combine(datetime.date.today(),
                                                                                        datetime.datetime.min.time()))
        till_datetime = self.request.query_params.get("till", datetime.datetime.now().replace(microsecond=0))
        print(from_datetime, till_datetime)
        cursor.execute('''select person_id, array_agg(t2.*) as catch_groups from (select * from collector_catch
                        left join "collector_person"
                        on ("collector_catch"."person_id" = "collector_person"."id")
                        where datetime between %s and %s
                        order by collector_catch.datetime, collector_catch.person_id asc ) t2 group by t2.person_id''',
                       (from_datetime, till_datetime))
        rows = cursor.fetchall()
        return rows


class PersonListView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class SinglePersonView(generics.ListAPIView):
    lookup_url_kwarg = "id"
    serializer_class = CatchSerializer

    def get_queryset(self, *args, **kwargs):
        print(self.request)
        print(self.request.query_params)
        print(args)
        print(kwargs)
        uid = self.kwargs.get(self.lookup_url_kwarg)
        print("UUID", uid)
        rows = Catch.objects.filter(person_id=uid)
        print(rows)
        return rows

    # def get(self, request, *args, **kwargs):
    #     print(request)
    #     print(args)
    #     print(kwargs)
    #     Catch.objects.get(person_id=kwargs.get("id"))
    #     return Response(status=status.HTTP_200_OK)


class GetLastImage(APIView):
    def post(self, request):
        if 'id' in request.data:
            prev_issue = Catch.objects.filter(camera_id=request.data['id']).order_by("-time")[1]
            serializer = CatchSerializer(prev_issue)
            return Response(serializer.data)
