from django.contrib import admin

# Register your models here.
from .models import Person, Car


admin.site.register(Person)
admin.site.register(Car)
