"""
    The Object-relational layer, including geospatial information
"""
from django.contrib.gis.db import models

UNIT_SRID = 4326

class Driver(models.Model):
    """
        Driver consist only of a driver ID and geographical coordinates.
    """
    driverId = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    point = models.PointField(srid=UNIT_SRID)

    class Meta:
        """ the postgres db table """
        db_table = 'driver'

    def __str__(self):
        return '%s %s %s' % (self.driverId, self.lat, self.lon)

class Shipment(models.Model):
    """
        Shipment consists of an ID, the shipment's geographical coordinates
        and a pointer to the driver that accepts the shipment.
    """
    shipmentId = models.BigIntegerField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    point = models.PointField(srid=UNIT_SRID)
    driver_accepted = models.ForeignKey('Driver',
                                        models.DO_NOTHING,
                                        db_column='driver',
                                        null=True)
    
    class Meta:
        """ the postgres db table """
        db_table = 'shipment'

    def __str__(self):
        return '%s %s %s %s' % (self.shipmentId,
                                self.lat,
                                self.lon,
                                self.driver_accepted if self.driver_accepted else '')

class Dispatch(models.Model):
    """
        Tracks which shipments have been dispatched to which drivers
    """
    id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey('Shipment',
                                 models.DO_NOTHING,
                                 db_column='dispatch_shipment')
    driver = models.ForeignKey('Driver',
                               models.DO_NOTHING,
                               db_column='dispatch_driver')
    accepted = models.BooleanField(null=True)

    class Meta:
        """ the postgres db table """
        db_table = 'dispatch'

    def __str__(self):
        return '%s %s %s %s' % (self.id,
                                self.shipment,
                                self.driver,
                                bool(self.accepted))
