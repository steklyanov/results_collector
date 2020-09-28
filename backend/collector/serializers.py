from rest_framework import serializers

from .models import Catch, Person


class PersonSerializer(serializers.Serializer):
    class Meta:
        model = Person
        fields = '__all__'


class CatchSerializer(serializers.Serializer):
    person = PersonSerializer

    class Meta:
        model = Catch
        fields = '__all__'
