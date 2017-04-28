# coding: utf-8

"""
    Clowder Streams API
"""

from pyclowder.client import ClowderClient
import logging


class StreamsApi(object):

    def __init__(self, client=None, host=None, key=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = ClowderClient(host=host, key=key, username=username, password=password)

    def streams_get(self):
        """
        Get the list of all available streams.

        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Getting all streams")
        try:
            return self.client.get("/geostreams/streams")
        except Exception as e:
            logging.error("Error retrieving sensor list: %s", e.message)


