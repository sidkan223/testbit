import logging
from pyclowder.geostreams.sensors import SensorsApi

sensor_id = ""


def test_sensors_post(caplog, host, key):
    global sensor_id
    caplog.setLevel(logging.DEBUG)
    client = SensorsApi(host=host, key=key)
    sensor_json = client.sensors_create_json("Test Sensor", 40.1149202, -88.2270582, 0)
    response = client.sensors_post(sensor_json)
    body = response.json()
    sensor_id = body['id']
    logging.info("Sensor %i posted", body['id'])
    assert response.status_code == 200 and body


def test_sensors_get(caplog, host, key):
    global sensor_id
    caplog.setLevel(logging.DEBUG)
    client = SensorsApi(host=host, key=key)
    response = client.sensor_get(sensor_id)
    sensor = response.json()
    logging.info("Sensor %s found" % sensor_id)
    assert response.status_code == 200 and sensor


def test_sensors_delete(caplog, host, key):
    global sensor_id
    caplog.setLevel(logging.DEBUG)
    client = SensorsApi(host=host, key=key)
    response = client.sensor_delete(sensor_id)
    sensor = response.json()
    logging.info("Sensor %s deleted" % sensor_id)
    assert response.status_code == 200 and sensor
