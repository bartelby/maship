"""
   Launch a thread to run the dispatcher periodically until all loaads have
   been dispatched, then print a summary of which load was dispatched to what driver.
   Note that in the real world periodic tasks like this would be performed by a
   more bullet-proof utility such as Celery,
""" 

import os
import time
import logging
import threading
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
            (1) Loop through shipments
            (2) For each shipment, dispatch to the three nearest drivers
            (3)
        """
        while True:
            # Shipments that have not been accepted by a driver:
            shipments = Shipment.objects.exclude(driver_accepted__is_null=False)
            for shipment in shipments:
                #TODO: filter out drivers that have not accepted any shipment and
                # that have rejected this shipment
                drivers = Driver.objects.exclude(shipment_accepted__is_null=False) \
                                                 .annotate(distance=Distance('point', shipment.point)) \
                                                 .order_by('distance')[:3]
                print("SHIPMENT", shipment)
                for driver in drivers:
                    print("driver", driver, "distance", driver.distance)

            
            time.sleep(10)

    def start(self):
        t = threading.Thread(target=self.run, args=(), kwargs={})
        t.run()
        print("Thread started")
        return

if __name__ == '__main__':
    dispatcher = Dispatcher()
    dispatcher.start()
