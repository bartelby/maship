"""
    This class encapsulates the dispatcher API endpoint.
    It takes a driverId in the URL and a shipmentId in
    the url's json and performs the dispatch, It returns
    a json object. 
    If driver and shipment ID are both valid, returns
    {
        response: 'Accepted' or 'Denied' (string),
        driverId: x (number),
        shipmentId: x (number)
    }
    Otherwise, returns 404 error if driver id is invalid
    Returns 400 error if shipment id is missing or invalid.

    The acceptance rate for shipments dispatch requests is 155
"""

from json import dumps as json_dumps

import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Driver, Shipment, Dispatch
from django.core.exceptions import ObjectDoesNotExist
import random

class Dispatcher(APIView):
    
    def get(self, request, driverId):
        shipmentId = request.GET.get('shipmentId', None)
        return self.dispatcher_guts(driverId, shipmentId)

    def post(self, request, driverId):
        shipmentId = request.POST.get('shipmentId', None)
        return self.dispatcher_guts(driverId, shipmentId)
    
    def dispatcher_guts(self, driver_id, shipment_id=None):
        driver = None
        shipment = None
        try:
            driver = Driver.objects.get(driverId=int(driver_id))
        except ObjectDoesNotExist:
            response = HttpResponse(json_dumps({"ERROR": "Invalid driver"}),
                                    content_type='application/json')
            response['response_code'] = 404
            return response
        try:
            shipment = Shipment.objects.get(shipmentId=shipment_id)
        except ObjectDoesNotExist:
            response = HttpResponse(json_dumps({"ERROR": "Invalid shipment"}),
                                    content_type='application/json')
            response['response_code'] = 400
            return response
        #WE HAVE A DRIVER AND A SHIPMENT.
        p_of_accept = random.randint(1, 101)
        accept = p_of_accept >= 85
        payload = {
            'response': 'Accepted' if accept else 'Denied',
            'driverId': driver_id,
            'shipmentId': shipment_id
        }
        response = HttpResponse(json_dumps(payload),
                                content_type='application/json')
        return response
                  
