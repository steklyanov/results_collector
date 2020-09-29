from rest_framework import serializers

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
