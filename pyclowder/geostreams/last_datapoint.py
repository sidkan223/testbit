# FUNCTION GETS LATEST DATAPOINT IN CLOWDER FOR A GIVEN STREAM (SENSOR)

import logging
from dateutil.parser import parse

from src.request_data.request_json import get_json, post_json

import src.config.config as config

medici = config.medici['url']
key = config.medici['key']
search_clowder_start_date = config.dates['search_clowder_start']

def last_datapoint(sensor_from_medici, stream_from_medici):
    latest_datapoint = None
    logging.info("Getting datapoints from Clowder at: " + medici + "datapoints?stream_id=" + str(stream_from_medici['id']) + "&since=" + str(search_clowder_start_date))

    datapoints_from_medici = get_json(medici + "datapoints?stream_id=" + str(stream_from_medici['id']) + "&since=" + str(search_clowder_start_date))
    logging.info("Done getting datapoints from Clowder")

    if isinstance(datapoints_from_medici, list) and len(datapoints_from_medici) >0:
        latest_datapoint = datapoints_from_medici[-1]
        start_date = parse(latest_datapoint['start_time']).strftime('%Y-%m-%d-%H-%M')
        logging.info("Fetched datapoints for " + sensor_from_medici['name'] + " starting on " + start_date)
        # first_datapoint = datapoints_from_medici[0]
        # print "first_datapoint: ", first_datapoint
    else:
        logging.debug("No datapoints exist on Medici yet for " + sensor_from_medici['name'])
    del datapoints_from_medici

    return latest_datapoint
