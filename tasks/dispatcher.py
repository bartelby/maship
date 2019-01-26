"""
   Launch a thread to run the dispatcher periodically until all loaads have
   been dispatched, then print a summary of which load was dispatched to what driver.
   Note that in the real world periodic tasks like this would be performed by a
   more bullet-proof utility such as Celery,
""" 

import os
import time
import logging
from json import loads as json_loads
from json import dumps as json_dumps
from django.contrib.gis.db.models.functions import Distance

import django
import urllib.parse
import urllib.request
from django.http import HttpResponse
from maship.maship import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maship.maship.settings')
django.setup()
from api.models import Driver, Shipment, Dispatch

HOST_URL = 'http://localhost:9000'

class Dispatcher(object):
    """
        This class periodically dispatches shipments to drivers.
        In a real world application. this would be managed by a more
        robust process, e.g. Celery.
    """

    def __init__(self):
        logging.basicConfig(
            filename='/home/maship/projects/maship.log',
            format='%(asctime)s %(levelname)s: %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def run(self, *args, **kwargs):
        """
            (1) Loop through shipments that have not yet been accepted
            (2) For each shipment, dispatch to the three nearest available drivers
            (3) Dispatch to the web server using /http://<host_url>:<port>/driver/<driverId/dispatch
                with a json string in the header: { 'shipmentId': <shipmentId> }
            (4) response will be either an error code or a json string including 'request': 'Accepted' or 'Denied', depending.
            (5) If denied, make an entry in Dispatch table for driver and shipment - this prevents redundant dispatches.
            (6) if accepted, also make entry in Dispatch table for drive and shipment.  
                Update Driver for shipment_accepted, update Shipment for driver_accepted.
            (7) continue until all shipments have been accepted.
        """
        shipments = Shipment.objects.exclude(driver_accepted__isnull=False)
        while shipments:
            # Shipments that have not been accepted by a driver:
            for shipment in shipments:
                dispatched = Dispatch.objects.filter(shipment=shipment).values('driver')
                ids = []
                for driver in dispatched:
                    ids.append(driver['driver'])
                drivers = Driver.objects.exclude(shipment_accepted__isnull=False) \
                                        .exclude(driverId__in=ids) \
                                        .annotate(distance=Distance('point', shipment.point)) \
                                        .order_by('distance')[:3]
                print("SHIPMENT", shipment)
                for driver in drivers:
                    print("dispatch to driver", driver, "distance", driver.distance)
                    self.dispatch(shipment, driver)
            shipments = Shipment.objects.exclude(driver_accepted__isnull=False)
            time.sleep(10)

    def dispatch(self, shipment, driver):
        """
            Create a dispatch for a shipment by hitting the following endpoint:
            POST http://challenge.shipwithbolt.com/driver/:driverId/dispatch
            Replace :driverId in the URL with the driverId you are dispatching to
            Pass in as the body in JSON format:
            {
                shipmentId: x (number)
            }
            If the driverId is invalid (does not exist in the driver JSON file), a 404 error will be returned.
            If the shipmentId is missing or invalid (does not exist in the shipment JSON file), a 400 error will be
        """
        url = '{0}/driver/{1}/dispatch/'.format(HOST_URL, driver.driverId)
        values = { 'shipmentId': shipment.shipmentId }
        data = urllib.parse.urlencode(values).encode('utf-8')
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        the_decision = json_loads(response.read())
        if the_decision.get('response', 'Denied') == 'Accepted':
            #FIXME: in production code put this in a txn
            Dispatch(driver=driver, shipment=shipment, accepted=True).save()
            driver.shipment_accepted=shipment
            driver.save()
            shipment.driver_accepted=driver
            shipment.save()
        else:
            Dispatch(driver=driver, shipment=shipment, accepted=False).save()

if __name__ == '__main__':
    dispatcher = Dispatcher()
    dispatcher.run()
