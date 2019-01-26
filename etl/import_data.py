"""
    Imports driver and shipment data from the json formatted files drivers.json and
    shipments.json and inserts the data into the driver and shipment tables in the
    geospatial dataabase maship. The files live in ./data directory.
"""
import os
from json import loads as json_loads
import django
from django.contrib.gis.geos import Point

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maship.maship.settings')
django.setup()
from api.models import Driver, Shipment

def import_data():
    """
        Reads json files from ./data directoruy and imports entries
        into Driver and Shipment tables in the database.
    """
    driver_filename = './data/drivers.json'
    shipment_filename = './data/shipments.json'
    # Import drivers
    data = ''
    with open(driver_filename) as _f:
        data = _f.read()
    if data:
        json_data = json_loads(data)
        for driver_id, loc_data in json_data.items():
            coordinates = loc_data['coordinates']
            lat = coordinates['latitude']
            lon = coordinates['longitude']
            #Create and save the Driver object
            kwargs = {
                'driverId': driver_id,
                'lat': lat,
                'lon': lon,
                'point': Point(lon, lat)
            }
            Driver(**kwargs).save()
            print('saved driver {0}, {1} {2}'.format(driver_id, lat, lon))

    # Import shipments
    data = ''
    with open(shipment_filename) as _f:
        data = _f.read()
    if data:
        json_data = json_loads(data)
        for shipment_id, ship_data in json_data.items():
            coordinates = ship_data['coordinates']
            lat = coordinates['latitude']
            lon = coordinates['longitude']
            #Create and save Shipment object
            kwargs = {
                'shipmentId': shipment_id,
                'lat': lat,
                'lon': lon,
                'point': Point(lon, lat)
            }
            Shipment(**kwargs).save()
            print("saved shipment {0} {1} {2}".format(shipment_id, lat, lon))

if __name__ == "__main__":
    import_data()
