from django.contrib import admin

# Register your models here.
from .models import student, bill

admin.site.register(student)
admin.site.register(bill)