import logging
import time

from request_json import post_json, get_json
from map_names import map_names
from time_transformers import time_transform

"""
Don't know why parsing datapoints posts datapoint and parser sensors and streams does not.
Probably because there is a lot of logic for checking if sensor/stream already exists.
Can it be combinded?
"""


# PARSE DATAPOINTS
# headers is a 1D list column headers
# data is a 2D list of rows of data
def parse_datapoints_from_list(headers,data,geocode,sensor_id,stream_id,site,clowder_key,clowder_url,owner=None,source=None,procedures=None,blocked_headers=None):
    count = 0
    while len(data) > 0:
        if count%300 == 0:
            logging.info(" [pyG.parse_geostream_objects] Posting datapoint " + str(count) + " for " + str(site) + " stream " +str(stream_id))
        count += 1
        datapoint = {
            'start_time': data[0][0],
            'end_time': data[0][0],
            'type': 'Feature',
            'geometry': {
                'type': "Point",
                'coordinates': [
                    geocode[1],
                    geocode[0],
                    geocode[2]
                ]
            },
            'stream_id': str(stream_id),
            'sensor_id': str(sensor_id),
            'sensor_name': str(site),
            'properties': {
                'site': site
            }
        }
        if owner != None:
            datapoint['properties']["owner"] = owner
        if source != None:
            datapoint['properties']['source'] = source
        if procedures != None:
            datapoint['properties']['procedures'] = procedures

        for i in range(1,len(data[0])): #time is the first parameter which is added above      
            if blocked_headers == None or headers[i] not in blocked_headers:
                datapoint['properties'][headers[i]] = data[0][i]

        url = clowder_url + "datapoints?key=" +clowder_key

        post_json(url, datapoint)

        data.pop(0)

        time.sleep(0.1)

def parse_single_datapoint(headers,data,start_time,geocode,sensor_id,stream_id,site,clowder_key,clowder_url,owner=None,source=None,procedures=None,blocked_headers=None):

    #logging.info(" [pyG.parse_geostream_objects] Posting datapoint for " + str(site) + " stream " +str(stream_id))
    if len(headers) != len(data):
        logging.warning(" [pyG.parser_geostream_objects] length of data and headers don't match - skipping")
        return
    datapoint = {
        'start_time': start_time,
        'end_time': start_time,
        'type': 'Feature',
        'geometry': {
            'type': "Point",
            'coordinates': [
                geocode[1],
                geocode[0],
                geocode[2]
            ]
        },
        'stream_id': str(stream_id),
        'sensor_id': str(sensor_id),
        'sensor_name': str(site),
        'properties': {
            'site': site
        }
    }
    if owner != None:
        datapoint['properties']["owner"] = owner
    if source != None:
        datapoint['properties']['source'] = source
    if procedures != None:
        datapoint['properties']['procedures'] = procedures

    for i in range(len(data)):
        if (blocked_headers == None or headers[i] not in blocked_headers) and data[i] not in [None,""]:
            datapoint['properties'][headers[i]] = data[i]

    url = clowder_url + "datapoints?key=" + clowder_key

    response_json = post_json(url, datapoint)


def parse_sensor(site,pretty_name,geocode,source_id,source_title,network=None):
    huc_url = "http://gltg.ncsa.illinois.edu/api/huc?lat="+str(geocode[0])+"&lng="+str(geocode[1])
    huc_data = get_json(huc_url)

    sensor = {
        "name": site,
        "type": "Feature",
        "properties": {
            "region": huc_data["huc4"]["code"],
            "huc": huc_data,
            "type": {
                "id": source_id,
                "title": source_title
            },
            "name": site,
            "popupContent": pretty_name
        },
        "geometry": {
            "type": "point",
            "coordinates": [geocode[1],geocode[0],geocode[2]]
    }
    }
    if network != None:
        sensor["properties"]["network"] = network

    return sensor

def parse_stream(sensor_id,site,pretty_name,geocode,source_id,source_title,network=None,data_type=None):
    huc_url = "http://gltg.ncsa.illinois.edu/api/huc?lat="+str(str(geocode[0]))+"&lng="+str(geocode[1])
    huc_data = get_json(huc_url)

    stream = {
        "name": site,
        "type": "Feature",
        "sensor_id": str(sensor_id),
        "geometry": {
            "type": "point",
            "coordinates": [geocode[1],geocode[0],geocode[2]]
    },
        "properties": {
            "region": huc_data["huc4"]["code"],
            "huc": huc_data,
            "type": {
                "id": source_id,
                "title": source_title
            },
            "name": site
        }
    }

    if network != None:
        stream["properties"]["network"] = network
    if data_type != None:
        stream['properties']['data_type'] = data_type

    return stream

def parse_json_to_sensor(dataIn):
    logging.info(" [parse_geostream_objects] getting huc codes ")
    huc_url = "http://gltg.ncsa.illinois.edu/api/huc?lat="+str(dataIn['value']['timeSeries'][0]['sourceInfo']["geoLocation"]["geogLocation"]["latitude"])+"&lng="+str(dataIn['value']['timeSeries'][0]['sourceInfo']["geoLocation"]["geogLocation"]["longitude"])
    huc_data = get_json(huc_url)
    logging.info(" [parse_geostream_objects] done getting huc codes ")



    sensor = {
        'name': dataIn['value']['timeSeries'][0]['sourceInfo']['siteCode'][0]['value'],
        'type': "Feature",
        'properties': {
            "region": huc_data["huc4"]["code"],
            'huc': huc_data,
            'type': {
                'id': 'usgs',
                'title': 'United States Geological Survey',
                'network': dataIn['value']['timeSeries'][0]['sourceInfo']['siteCode'][0]['network']
            },
            'name': dataIn['value']['timeSeries'][0]['sourceInfo']['siteCode'][0]['value'],
            'popupContent': dataIn['value']['timeSeries'][0]["sourceInfo"]['siteName']
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [
                dataIn['value']['timeSeries'][0]['sourceInfo']["geoLocation"]["geogLocation"]["longitude"],
                dataIn['value']['timeSeries'][0]['sourceInfo']["geoLocation"]["geogLocation"]["latitude"],
                0]
        }
    }

    return sensor

def parse_json_to_stream(sensorData, sourceUrl,data_type=None):
    # pprint.pprint(sensorData)
    stream = {
        'name': sensorData['name'],
        'type': "Feature",
        'properties': {
            'source': sourceUrl,
            'huc': sensorData['properties']['huc'],
            'region': sensorData['properties']['region'],
            'type': sensorData['properties']['type']
        },
        'sensor_id': str(sensorData['id']),
        'geometry': sensorData['geometry']
    }

    if data_type != None:
        stream["properties"]['data_type'] = data_type

    # print "/////"
    # pprint.pprint(stream)
    # exit()

    return stream

def parse_rdb_to_datapoints(dataIn, sensor, stream):
    logging.info(" [parse_geostream_objects] Start creating datapoints JSON")

### READ DATA INTO ROWS EXCLUDING LINES STARTING WITH '#'
    rows = []
    lineOfText = ""

    for i in range(len(dataIn)):
        if dataIn[i] != "\n":
            lineOfText += dataIn[i]
        else:
            if lineOfText[0] != "#":
                rows.append(lineOfText)
            lineOfText = ""

#SPLIT ROWS INTO LIST field_values, SEPARATE THE FISRT ROW (headers) AND SECOND ROW (data specs)
    headerText = rows.pop(0)
    header = headerText.split("\t")
    dataSpecsText = rows.pop(0)
    dataSpecs = dataSpecsText.split("\t")

    field_data = []
    for i in range(len(rows)):
        field_data.append(rows[i].split("\t"))

    del dataIn
    del rows

    for i in range(len(header)):
        header[i] = map_names(header[i])

    header.pop(3)

#COMBINE TIME (field_data[i][2]) AND TIMEZONE (field_data[i][3]) INTO ONE FIELD (field_data[i][2])
    for i in range(len(field_data)):
        field_data[i][2] = time_transform(field_data[i][2],field_data[i][3])
        field_data[i].pop(3)

# CREATE DATAPOINTS IN JSON
    logging.info("Starting creation of datapoints JSON")
    datapoints_out = []
    while len(field_data) > 0: 
        datapoint = {
            'start_time': field_data[0][2],
            'end_time': field_data[0][2],
            'type': 'Feature',
            'geometry': {
                'type': sensor['geometry']['type'],
                'coordinates': [
                    sensor['geometry']['coordinates'][0],
                    sensor['geometry']['coordinates'][1],
                    sensor['geometry']['coordinates'][2]
                ]
            },
            'stream_id': str(stream['id']),
            'sensor_id': str(sensor['id']),
            'sensor_name': str(sensor['name']),
            'properties': {
                'source': "http://waterdata.usgs.gov/nwis",
                'procedures': "http://pubs.usgs.gov/fs/2007/3043/FS2007-3043.pdf",
                'owner': "usgs",
                'site': field_data[0][1]
            }
        }

        for j in range(3,len(field_data[0]),2):
            if field_data[0][j] not in [None,""," ","eqp","ice","***","ICE","Eqp","Fld","Ssn","Dis","Ice","Bkw"]:
                datapoint['properties'][header[j]] = float(field_data[0][j])
                datapoint['properties'][header[j+1]] = field_data[0][j+1]
        field_data.pop(0)
        datapoints_out.append(datapoint)

    logging.info(" [parse_geostream_objects] Done creating datapoints JSON")
    return datapoints_out

