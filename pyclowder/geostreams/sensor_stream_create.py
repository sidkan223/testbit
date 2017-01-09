import logging
from time import strftime
from request_json import get_json, post_json

def sensor_create(sensor,site,key,medici):
    sensor_id = None
    sensor_from_medici = get_json(medici + "sensors?geocode=" +
                         str(sensor['geometry']['coordinates'][1]) + ',' +
                         str(sensor['geometry']['coordinates'][0]) + ',' +
                         str(sensor['geometry']['coordinates'][2]))

    if sensor_from_medici:
        logging.info("Found sensor " + str(site) + " on Medici.")
        sensor_from_medici = sensor_from_medici[0]
        sensor_id = sensor_from_medici['id']
    else:
        logging.info(" [pyG.sensor_stream_create " + strftime('%Y-%m-%d %H:%M:%S') + "] POSTing sensor " + str(site) + " to Medici...")
        sensor_from_medici = post_json(medici + "sensors?key=" + key, sensor)
        if sensor_from_medici:
            sensor_from_medici = get_json(medici + "sensors?geocode=" +
                         str(sensor['geometry']['coordinates'][1]) + ',' +
                         str(sensor['geometry']['coordinates'][0]) + ',' +
                         str(sensor['geometry']['coordinates'][2]))
            if isinstance(sensor_from_medici, list):
                sensor_from_medici = sensor_from_medici[0]
                sensor_id = sensor_from_medici['id']
        else:
            logging.warning("Could not POST sensor to Medici. Exiting...")
            exit()

    return sensor_id, sensor_from_medici


def stream_create(sensor_id,site,stream,key,medici):
    stream_id = None
    stream_from_medici = get_json(medici + "streams?stream_name=" + str(stream['name']))
  
    if isinstance(stream_from_medici, list):
        stream_from_medici = stream_from_medici[0]
        stream_id = stream_from_medici['id']
    else:
        stream_from_medici = post_json(medici + "streams?key=" +key,stream)
        if stream_from_medici:
            stream_from_medici = get_json(medici + "streams?stream_name=" + str(stream['name']))
            if isinstance(stream_from_medici,list):
                stream_from_medici = stream_from_medici[0]
                stream_id = stream_from_medici['id']
        else:
            exit()
    return stream_id, stream_from_medici


