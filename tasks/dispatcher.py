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
from maship.maship import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maship.maship.settings')
django.setup()
from api.models import Driver, Shipment, Dispatch

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
            (3)
        """
        shipments = Shipment.objects.exclude(driver_accepted__isnull=False)
        while shipments:
            # Shipments that have not been accepted by a driver:
            for shipment in shipments:
                dispatched = Dispatch.objects.filter(shipment=shipment).values('driver')
                ids = [driver.driverId for driver in dispatched]
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
        pass

if __name__ == '__main__':
    dispatcher = Dispatcher()
    dispatcher.run()
