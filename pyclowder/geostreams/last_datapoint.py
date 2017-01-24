import logging
from dateutil.parser import parse

from request_json import get_json, post_json

def last_datapoint(sensor_from_medici, stream_from_medici):
    """Get latest datapoint for a given stream without relying on the stats."""
    global clowder_host, clowder_key
    search_clowder_start_date = ""
    latest_datapoint = None
    logging.info("Getting datapoints from Clowder at: " + clowder_host + "datapoints?stream_id=" + str(
        stream_from_medici['id']) + "&since=" + str(search_clowder_start_date))

    datapoints_from_medici = get_json(
        clowder_host + "datapoints?stream_id=" + str(stream_from_medici['id']) + "&since=" + str(search_clowder_start_date))
    logging.info("Done getting datapoints from Clowder")

    if isinstance(datapoints_from_medici, list) and len(datapoints_from_medici) > 0:
        latest_datapoint = datapoints_from_medici[-1]
        start_date = parse(latest_datapoint['start_time']).strftime('%Y-%m-%d-%H-%M')
        logging.info("Fetched datapoints for " + sensor_from_medici['name'] + " starting on " + start_date)
        # first_datapoint = datapoints_from_medici[0]
        # print "first_datapoint: ", first_datapoint
    else:
        logging.debug("No datapoints exist on Medici yet for " + sensor_from_medici['name'])
    del datapoints_from_medici

    return latest_datapoint
