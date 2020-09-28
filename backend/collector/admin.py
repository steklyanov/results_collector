from django.contrib import admin

from .models import Person, Catch

# Register your models here.
admin.site.register(Catch)
admin.site.register(Person)
