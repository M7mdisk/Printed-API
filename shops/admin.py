from django.contrib import admin
from .models import Profile, Shop, Order, Type
from django.contrib.gis.db import models
from leaflet.admin import LeafletGeoAdmin

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('uuid','total')
# Register your models here.
admin.site.register(Profile)
admin.site.register(Shop,LeafletGeoAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Type)
