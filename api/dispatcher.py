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

class Dispatcher(APIView):
    
    def get(self, request):
        driver_id = request.GET.get('driver', None)
        return self.dispatcher(driver_id)

    def dispatcher(driver_id, shipment_id=None):
        if not driver_id:
            response = HttpResponse(json_dumps({"ERROR": 'No driver specified'}),
                                    content_type='application/json')
            response['status_code'] = 404
            return response
        driver = Driver.objects.get(driverId=driver_id)
        if not driver:
            response = HttpResponse(json_dumps({"ERROR": 'Invalid driver'}),
                                    content_type='application/json')
            response['status_code'] = 404
            return response
        respnse = HttpResposnse(json_dumps({'SUCCESS': 'Hello Peter!'}),
                                content_type='application/json')
        return response
                  
