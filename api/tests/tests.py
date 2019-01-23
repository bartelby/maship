"""
   Test setup for geosatial databse
"""

from django.test import TestCase
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from api.models import Driver, Shipment, Dispatch

class Test(TestCase):

    def make_driver(self, driver_id, lon, lat, point):
        kwargs = {
            'driverId': driver_id,
            'lon': lon,
            'lat': lat,
            'point': point
        }
        Driver(**kwargs).save()

    def make_shipment(self, shipment_id, lon, lat, point, driver=None):
        kwargs = {
            'shipmentId': shipment_id,
            'lon': lon,
            'lat': lat,
            'point': point,
            'driver_accepted': driver
        }
        Shipment(**kwargs).save()

    def make_dispatch(self, driver, shipment, accepted=None):
        kwargs = {
            'driver': driver,
            'shipment': shipment,
            'accepted': accepted
        }
        Dispatch(**kwargs).save()

    def test_100_driver(self):
        boston = Point(-71.0589, 42.3601)
        self.make_driver(3, -71.06, 42.36, boston)
        los_angeles = Point(-118.2437, 34.0522)
        self.make_driver(1, -118.24, 34.05, los_angeles)
        cleveland = Point(-81.69, 41.50)
        self.make_driver(72, -81.69, 41.5, cleveland)
        actual =  [driver.driverId for driver in Driver.objects.annotate(distance=Distance('point', boston)).order_by('distance')]
        expected = [3, 72, 1]
        self.assertEqual(actual, expected)

    def test_200_shipment(self):
        boston = Point(-71.0589, 42.3601)
        self.make_driver(1, -71.06, 42.36, boston)
        boston_driver = Driver.objects.get(driverId=1)
        cambridge = Point(-71.11, 42.37)
        newton = Point(-71.21, 42.34)
        self.make_shipment(9999999999, -71.11, 42.37, cambridge)
        self.make_shipment(8888888888, -71.21, 42.34, newton)
        self.make_shipment(9999999998, -71.11, 42.37, cambridge, boston_driver)
        actual = len(Shipment.objects.all())
        self.assertEquals(actual, 3)
        # Test to find only shipments without driver_accepted (careful of double negative!)/Users/bartelby 
        actual = len(Shipment.objects.exclude(driver_accepted__isnull=False))
        self.assertEquals(actual, 2)
        # Test to find only shipments with driver_accepted
        actual = len(Shipment.objects.exclude(driver_accepted__isnull=True))
        self.assertEquals(actual, 1)

    def test_300_dispatch(self):
        boston = Point(-71.06, 42.36)
        newton = Point(-71.21, 42.34)
        cleveland = Point(-81.69, 41.5) 
        self.make_driver(1, 71.06, 42.36, boston)
        self.make_shipment(1, -71.21, 42.34, newton)
        self.make_shipment(2, -81.69, 41.5, cleveland)
        boston_driver = Driver.objects.get(driverId=1)
        newton_shipment = Shipment.objects.get(shipmentId=1)
        cleveland_shipment = Shipment.objects.filter(point=cleveland).first()
        self.make_dispatch(boston_driver, newton_shipment, True)
        self.make_dispatch(boston_driver, cleveland_shipment, False)
        actual = len(Dispatch.objects.all())
        self.assertEquals(actual, 2)
        accepted = Dispatch.objects.filter(accepted=True).first()
        self.assertEqual(accepted.driver, boston_driver)
        rejected = Dispatch.objects.filter(accepted=False).first()
        self.assertEqual(rejected.shipment, cleveland_shipment)
