import logging
from pyclowder.client import ClowderClient


class GeostreamsClient(object):
    """Client to Clowder API to store connection information."""
    logger = logging.getLogger(__name__)

    def __init__(self, host, key):
        """
         Create an instance of `GeostreamsClient`. Set `self.client` to the underlying `ClowderClient` using the
         delegation pattern.

         :param string host: The root host url of the specific geostreaming API we are connecting to.
         :param string key: The API key used to write to the API.
         """
        self.host = host
        self.key = key
        self.client = ClowderClient(host=host, key=key)

    def version(self):
        r = self.client.version()
        return r

    def get_sensors_list(self):
        """
         Get the list of all available sensors.

         :return: Full list of sensors.
         :rtype: JSON
         """
        self.logger.debug("Getting all sensors")
        try:
            return self.client.get("/geostreams/sensors")
        except Exception as e:
            self.logger.error("Error retrieving sensor list: %s", e.message)
            self.logger.debug("Done retrieving sensors ")

    def add_datapoint(self, stream):
        """Add a datapoint to a stream"""
        pass