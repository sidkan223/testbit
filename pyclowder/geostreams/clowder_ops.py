import logging
from datetime import datetime
import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta

from request_json import get_json


def update_sensor_statistics(clowder_url, site, sensor_id, key):
    """Update derived sensor statistics such as start time, end time, parameters listing."""
    logging.debug("Updating sensor with name=" + str(site) + " and id=" + str(sensor_id))
    try:
        url = clowder_url + "sensors/" + str(sensor_id) + "/update?key=" + str(key)
        get_json(url)
    except:
        pass
    logging.debug("Done updating sensor " + str(site))


def invalidate_cache(clowder_url, site, sensor_id, key):
    """Invalidate sensor cache."""
    logging.debug("Invalidating cache for sensor with name=" + str(site) + " and id=" + str(sensor_id))
    try:
        url = clowder_url + "cache/invalidate?sensor_id=" + str(sensor_id) + "&key=" + str(key)
        requests.get(url)
    except:
        pass
    logging.debug("Done invalidating cache for sensor " + str(site))


def get_last_datapoint_time(clowder_url, stream_id):
    """Get last datapoint from Clowder (if it exists) and set start time for parsing at that time. """

    # get stream info
    url = clowder_url + "streams/" + str(stream_id)
    return get_json(url)['end_time']


def prime_cache(sensor_id, clowder_url, clowder_key):
    """Prime the cache of a specific sensor."""
    logging.info(" Caching datapoints for sensor with id: " + str(sensor_id))

    url = clowder_url + "sensors/" + str(sensor_id) + "?key=" + clowder_key
    r = requests.get(url)

    # Calculate time in days between start and end date of sensor info
    delta_days = (
        datetime.strptime(r.json()['max_end_time'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(
            r.json()['min_start_time'],
            "%Y-%m-%dT%H:%M:%SZ")).days

    # Calculate time in years between start and end date of sensor info
    delta_years = relativedelta(parser.parse(r.json()['max_end_time']), parser.parse(r.json()['min_start_time'])).years

    if delta_years > 100:
        time_bin = 'decade'
    elif delta_years > 50:
        time_bin = 'lustrum'
    elif delta_years > 25:
        time_bin = 'year'
    elif delta_years > 10:
        time_bin = 'season'
    elif delta_years > 1:
        time_bin = 'month'
    else:
        if delta_days > 14:
            time_bin = 'day'
        elif delta_days > 3:
            time_bin = 'hour'
        else:
            time_bin = 'minute'
    try:
        url = clowder_url + "datapoints/bin/" + str(time_bin) + "/1?sensor_id=" + str(sensor_id)
        logging.info("Priming cache for sensor " + str(url))
        requests.get(url)
    except:
        pass
    logging.info(" Done caching datapoints for sensor with id: " + str(sensor_id))
