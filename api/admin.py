from django.contrib import admin
from .models import Driver, Shipment, Dispatch

admin.site.register(Driver)
admin.site.register(Shipment)
admin.site.register(Dispatch)
