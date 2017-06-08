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

    def datapoint_latest_get(self, sensor_id, stream_id, since=None):
        """
        Get latest datapoint for a given stream by retrieving datapoint since a recent date and then grabbing
        the latest one.

        TODO: this should be an API endpoint
        """
        latest_datapoint = None
        # logging.info("Getting datapoints for stream %s since %s " % stream_id, since)
        if since is None:
            url = "/geostreams/datapoints?stream_id=%s" % stream_id
        else:
            url = "/geostreams/datapoints?stream_id=%s&since=%s" % stream_id, since
        try:
            datapoints = self.client.get_json(url)
        except Exception as e:
            logging.error("Error getting datapoints for stream %s since %s" % stream_id, since, e.message)

        if isinstance(datapoints, list) and len(datapoints) > 0:
            latest_datapoint = datapoints[-1]
            start_date = parse(latest_datapoint['start_time']).strftime('%Y-%m-%d-%H-%M')
            logging.info("Fetched datapoints for " + str(sensor_id) + " starting on " + start_date)
        else:
            logging.debug("No datapoints exist for " + str(sensor_id))

        return latest_datapoint

    def datapoint_create_json(self, start_time, end_time, longitude, latitude, sensor_id, stream_id, sensor_name,
                              property_ids, properties, owner=None, source=None, procedures=None, elevation=0):
        datapoint = {
            'start_time': start_time,
            'end_time': end_time,
            'type': 'Feature',
            'geometry': {
                'type': "Point",
                'coordinates': [
                    longitude,
                    latitude,
                    elevation
                ]
            },
            'stream_id': str(stream_id),
            'sensor_id': str(sensor_id),
            'sensor_name': str(sensor_name),
            'properties': {
                'site': sensor_name
            }
        }
        #
        if owner is not None:
            datapoint['properties']["owner"] = owner
        if source is not None:
            datapoint['properties']['source'] = source
        if procedures is not None:
            datapoint['properties']['procedures'] = procedures

        for i in range(len(property_ids)):
            datapoint['properties'][property_ids[i]] = properties[i]

        return datapoint