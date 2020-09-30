from abc import ABC

from rest_framework import serializers

import json
import ast

from .models import Catch, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CatchSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Catch
        fields = ['image', 'datetime', 'camera_serial', 'person']


class NestedCatchesSerializer(serializers.Serializer):
    dict_fields = ["id", "img_path", "datetime", "cam_id", "name", "external_id"]

    @staticmethod
    def string_tuple_to_dict(string: str):
        string = string[1:-1].replace('"', '')
        string = string.split(',')
        del string[4:6]
        return dict(zip(NestedCatchesSerializer.dict_fields, string))

    def to_representation(self, instance):
        print(instance)
        cell = [row for row in ast.literal_eval(instance[1])]
        return {instance[0]: [self.string_tuple_to_dict(string) for string in cell]}
