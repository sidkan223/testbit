# coding: utf-8

"""
    Clowder Datapoints API
"""

from pyclowder.client import ClowderClient
import logging
from dateutil.parser import parse


class DatapointsApi(object):

    def __init__(self, client=None, host=None, key=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = ClowderClient(host=host, key=key, username=username, password=password)

    def datapoint_post(self, datapoint):
        """
        Add a datapoint.

        :return: If successful or not.
        :rtype: `requests.Response`
        """
        logging.debug("Adding datapoint")
        try:
            return self.client.post("/geostreams/datapoints", datapoint)
        except Exception as e:
            logging.error("Error adding datapoint %s: %s" % datapoint, e.message)

    def datapoints_count_by_sensor_get(self, sensor_id):
        """
        Get the list of all available sensors.

        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Counting datapoints by sensor")
        try:
            return self.client.get("/geostreams/datapoints?sensor_id=%s&onlyCount=true" % sensor_id)
        except Exception as e:
            logging.error("Error counting datapoints by sensor %s: %s" % sensor_id, e.message)

    def datapoint_latest_get(self, sensor_id, stream_id, since):
        """
        Get latest datapoint for a given stream by retrieving datapoint since a recent date and then grabbing
        the latest one.

        TODO: this should be an API endpoint
        """
        latest_datapoint = None
        logging.info("Getting datapoints for stream %s since %s " % stream_id, since)

        try:
            datapoints = self.client.get_json("/geostreams/datapoints?stream_id==%s&since=%s" % stream_id, since)
        except Exception as e:
            logging.error("Error getting datapoints for stream %s since %s" % stream_id, since, e.message)

        if isinstance(datapoints, list) and len(datapoints) > 0:
            latest_datapoint = datapoints[-1]
            start_date = parse(latest_datapoint['start_time']).strftime('%Y-%m-%d-%H-%M')
            logging.info("Fetched datapoints for " + sensor_id + " starting on " + start_date)
        else:
            logging.debug("No datapoints exist for " + sensor_id)

        return latest_datapoint