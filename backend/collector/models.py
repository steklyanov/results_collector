from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    ex_id = models.CharField(max_length=50, unique=True)


class Catch(models.Model):
    image = models.ImageField(upload_to='catches')
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    camera_serial = models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
