# coding: utf-8

"""
    Clowder Sensors API
"""

from pyclowder.client import ClowderClient
import logging
from request_json import get_json


class SensorsApi(object):

    def __init__(self, client=None, host=None, key=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = ClowderClient(host=host, key=key, username=username, password=password)

    def sensors_get(self):
        """
        Get the list of all available sensors.

        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Getting all sensors")
        try:
            return self.client.get("/geostreams/sensors")
        except Exception as e:
            logging.error("Error retrieving sensor list: %s", e.message)

    def sensor_get(self, sensor_id):
        """
        Get a specific sensor by id.

        :return: Sensor object as JSON.
        :rtype: `requests.Response`
        """
        logging.debug("Getting sensor %s" % sensor_id)
        try:
            return self.client.get("/geostreams/sensors/%s" % sensor_id)
        except Exception as e:
            logging.error("Error retrieving sensor %s: %s" % sensor_id, e.message)


    def sensor_post(self, sensor):
        """
        Create sensor.

        :return: If successful or not.
        :rtype: `requests.Response`
        """
        logging.debug("Adding sensor")
        try:
            return self.client.post("/geostreams/sensors", sensor)
        except Exception as e:
            logging.error("Error adding datapoint %s" % sensor, e.message)


    def sensor_delete(self, sensor_id):
        """
        Delete a specific sensor by id.

        :return: If successfull or not.
        :rtype: `requests.Response`
        """
        logging.debug("Deleting sensor %s" % sensor_id)
        try:
            return self.client.delete("/geostreams/sensors/%s" % sensor_id)
        except Exception as e:
            logging.error("Error retrieving sensor %s: %s" % sensor_id, e.message)

    def sensor_create_json(self, name, longitude, latitude, elevation, popupContent, region):
        """Create sensor definition in JSON"""
        sensor = {
            "name": name,
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    longitude,
                    latitude,
                    elevation
                ]
            },
            "properties": {
                "name": name,
                "popupContent": popupContent,
                "region": region
            }
        }
        return sensor

    def sensor_statistics_post(self, sensor_id):
        """
        Update sensor statistics.

        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Updating sensor statistics")
        try:
            # TODO this should be a PUT on the API side, not a GET
            return self.client.get_auth("/geostreams/sensors/%s/update" % sensor_id)
        except Exception as e:
            logging.error("Error updating sensor statistics for sensor %s: %s" % sensor_id, e.message)

    def sensor_get_huc(self,latitude,longitude):
        huc_url = "http://gltg.ncsa.illinois.edu/api/huc?lat=" + str(latitude) + "&lng=" + str(longitude)
        huc_data = get_json(huc_url)
        return huc_data