from rest_framework import serializers
from .models import Driver, Shipment, Dispatch

class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment
        fields = '__all__'

class DispatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dispatch
        fields = '__all__'
