from .models import Catch, Person
from .serializers import NestedCatchesSerializer, CatchSerializer, PersonSerializer

from django.core.files.base import ContentFile
from django.db import connection
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import os
import names
import base64
import time
import datetime
from openpyxl import Workbook
from shutil import copy, make_archive, rmtree


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
        from_time = datetime.datetime.fromtimestamp(int(self.request.query_params.get("from",
                                                                             int(datetime.datetime.now().timestamp()))))
        till_time = datetime.datetime.fromtimestamp(int(self.request.query_params.get("till",
                                                                             int(datetime.datetime.now().timestamp()))))
        cursor = connection.cursor()
        cursor.execute('''select person_id, array_agg(t2.*) as catch_groups from (select * from collector_catch
                        left join "collector_person"
                        on ("collector_catch"."person_id" = "collector_person"."id")
                        where datetime between %s and %s
                        order by collector_catch.datetime, collector_catch.person_id asc ) t2 group by t2.person_id''',
                       (from_time, till_time))
        rows = cursor.fetchall()
        print(rows)
        return rows

    def list(self, request, *args, **kwargs):
        is_report = self.request.query_params.get("report", False)
        if is_report:
            from_time = datetime.datetime.fromtimestamp(int(self.request.query_params.get("from",
                                                                                          int(datetime.datetime.now().timestamp()))))
            till_time = datetime.datetime.fromtimestamp(int(self.request.query_params.get("till",
                                                                                      int(datetime.datetime.now().timestamp()))))
            catches = Catch.objects.filter(datetime__date__gte=from_time, datetime__date__lte=till_time).order_by('datetime')
            print(catches)
            wb = Workbook()
            ws = wb.active
            ws.title = 'Пассажиропоток'
            idx = 1
            for catch in catches:
                ws['A' + str(idx + 1)] = str(catch.person.name)
                ws['B' + str(idx + 1)] = str(catch.person.ex_id)
                ws['C' + str(idx + 1)] = str(catch.datetime)
                idx += 1
            wb.save('documents/sheet.xlsx')
            make_archive("document", 'zip', "documents")
            response = HttpResponse(open("document.zip", 'rb'), content_type='application/zip')
            return response
        return super().list(request, args, kwargs)


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


class CreateSheetView(generics.ListAPIView):
    def get(self, request):
        try:
            os.stat("documents")
        except Exception as e:
            os.mkdir("documents")

        from_dt, to_dt = self.request.query_params.get("from"), self.request.query_params.get("to")
        if from_dt is None or to_dt is None:
            return Response(status=400, data={"error": "Please provide to and from"})

        date_start = datetime.fromtimestamp(int(from_dt))
        date_finish = datetime.fromtimestamp(int(to_dt))

        dates = []

        delta = date_finish.date() - date_start.date()
        for i in range(delta.days + 1):
            day = date_start.date() + datetime.timedelta(days=i)
            dates.append(day)

        wb = Workbook()
        ws = wb.active
        ws.title = 'Пассажиропоток'
        ws['A1'] = "(YYYY-MM-DD-HH-MM-SS)"
        ws['B1'] = "ID камеры"
        ws['C1'] = "Количество пассажиров"
        ws['D1'] = "Уникальные"
        ws['E1'] = "Распознаные"
        total = 0

        catches = Catch.objects.filter(time__date__gte=date_start, time__date__lte=date_finish, camera=camera) \
            .select_related("camera", "person").order_by('time')
        recognized = list(filter(lambda x: x.person is not None, catches))

        for index, d in enumerate(dates):
            date_catches = list(filter(lambda x: x.time.date() == d, catches))
            date_recognized = list(filter(lambda x: x.person is not None, date_catches))
            unique = set(date_recognized)

            total += len(date_catches)
            ws['A' + str(index + 2)] = str(d)
            ws['B' + str(index + 2)] = "2"
            ws['C' + str(index + 2)] = len(date_catches)
            ws['D' + str(index + 2)] = len(date_catches) - (len(date_recognized) - len(unique))
            ws['E' + str(index + 2)] = len(date_recognized)
        ws['A' + str(len(dates) + 3)] = "Общаяя сумма"
        ws['C' + str(len(dates) + 3)] = total

        ws3 = wb.create_sheet("New_sheet")
        ws3.title = 'Уникальные'
        ws3['A1'] = "(YYYY-MM-DD-HH-MM-SS)"
        ws3['B1'] = "ID камеры"
        ws3['C1'] = "ID пассажира"
        ws3.column_dimensions['A'].width = 20
        ws3.column_dimensions['B'].width = 20
        ws3.column_dimensions['C'].width = 20
        unique = set([i for i in recognized])
        print(len(unique))
        print(len(recognized))
        for index, catch in enumerate(unique):
            ws3['A' + str(index + 2)] = catch.time
            ws3['B' + str(index + 2)] = catch.camera.id
            ws3['C' + str(index + 2)] = catch.person.id

        ws2 = wb.create_sheet("New_sheet")
        ws2.title = 'Распознавание'
        ws2['A1'] = "(YYYY-MM-DD-HH-MM-SS)"
        ws2['B1'] = "ID камеры"
        ws2['C1'] = "ID пассажира"
        ws2['D1'] = "Фото в момент прохода"
        ws2['E1'] = "Детектирование"
        ws2['F1'] = "% сходства с эталоном"
        ws2.column_dimensions['A'].width = 20
        ws2.column_dimensions['B'].width = 20
        ws2.column_dimensions['C'].width = 20
        ws2.column_dimensions['D'].width = 20
        ws2.column_dimensions['E'].width = 20
        ws2.column_dimensions['F'].width = 20
        for index, catch in enumerate(recognized):
            time = str(catch.time.time()).split(":")
            photo_name = str(catch.time.date()) + "_" + str(time[0]) + str(time[1]) + \
                         str(time[2][:2]) + "0000" + str(catch.person.id) + ".jpg"
            ws2['A' + str(index + 2)] = catch.time
            ws2['B' + str(index + 2)] = catch.camera.id
            ws2['C' + str(index + 2)] = "0000" + str(catch.person.id)
            ws2['D' + str(index + 2)] = photo_name
            ws2['E' + str(index + 2)] = "Да"
            ws2['F' + str(index + 2)] = str(0)
            # ws2['F' + str(index + 2)] = str(int(catch.score * 150))
            print(catch.image.path)
            try:
                print(photo_name)
                copy(catch.image.path, "documents/" + photo_name)
            except Exception as e:
                print(e, catch.id)
            print("Im done", index)
        wb.save('documents/sheet.xlsx')
        make_archive("document", 'zip', "documents")

        if os.path.exists("documents") and os.path.isdir("documents"):
            rmtree("documents")
        try:
            os.stat("documents")
        except:
            os.mkdir("documents")

        response = HttpResponse(open("document.zip", 'rb'), content_type='application/zip')
        return response
