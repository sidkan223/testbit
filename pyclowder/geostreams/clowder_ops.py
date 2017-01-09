import logging
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil import tz, parser
from datetime import date, datetime
import requests
import time

# import greon.config as config
from pyGeodashboard2.request_json import get_json

def update_sensor(clowder_url,site,sensor_id,key):
    logging.debug("Updating sensor with name=" + str(site) + " and id=" + str(sensor_id))
    try:
        url = clowder_url + "sensors/" + str(sensor_id) + "/update?key=" + str(key)
        r = get_json(url)
    except:
        pass
    logging.debug("Done updating sensor " +  str(site))

def invalidate_cache(clowder_url,site,sensor_id,key):
    logging.debug("Invalidating cache for sensor with name=" + str(site) + " and id=" + str(sensor_id))
    try:

        url = clowder_url + "cache/invalidate?sensor_id="+str(sensor_id)+"&key=" + str(key)
        logging.debug(url)
        r = requests.get(url)      
    except:
        pass
    logging.debug("Done invalidating cach for sensor " +  str(site))

def get_last_datapoint_time(clowder_url,stream_id):
    # GET LAST DATAPOINT FROM CLOWDER (IF EXISTS) AND SET START TIME FOR PARSING AT THAT TIME (OR CONFIG START TIME)

    url = clowder_url + "streams/" + str(stream_id)
    latest_datapoint = get_json(url)
       
    # quick fix for clowder returning stream end_time in different format
    if latest_datapoint == None or latest_datapoint['end_time'] == None:
        return None
    elif latest_datapoint['end_time'][-4:] == '6:00':
        latest_datapoint['end_time'] = latest_datapoint['end_time'][:-6] 
        latest_datapoint['end_time'] = datetime.strptime(latest_datapoint['end_time'],"%Y-%m-%dT%H:%M:%S") + relativedelta(hours=6)
        latest_datapoint['end_time'] = unicode((str(latest_datapoint['end_time'].date()) + "T" + str(latest_datapoint['end_time'].time()) + "Z"),"utf-8" )
    elif latest_datapoint['end_time'][-4:] == '5:00':
        latest_datapoint['end_time'] = latest_datapoint['end_time'][:-6] 
        latest_datapoint['end_time'] = datetime.strptime(latest_datapoint['end_time'],"%Y-%m-%dT%H:%M:%S") + relativedelta(hours=5)
        latest_datapoint['end_time'] = unicode((str(latest_datapoint['end_time'].date()) + "T" + str(latest_datapoint['end_time'].time()) + "Z"),"utf-8" ) 

    return latest_datapoint['end_time']

def prime_cache(sensor_id,clowder_url,clowder_key):
    logging.info(" Caching datapoints for sensor with id: " + str(sensor_id))

    # GET TIME IN YEARS BETWEEN END AND START DATE FOR SENSOR
    url = clowder_url + "sensors/" + str(sensor_id) +"?key=" + clowder_key
    r  = requests.get(url)

    delta_days = (datetime.strptime(r.json()['max_end_time'],"%Y-%m-%dT%H:%M:%SZ")-datetime.strptime(r.json()['min_start_time'],"%Y-%m-%dT%H:%M:%SZ")).days
    delta_years = relativedelta(parser.parse(r.json()['max_end_time']),parser.parse(r.json()['min_start_time'])).years

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
        url = clowder_url + "datapoints/bin/" + str(time_bin) + "/1?sensor_id=" +str(sensor_id)
        logging.info("PRIMING URL: " + str(url))
        r  = requests.get(url)
    except:
        pass
    logging.info(" Done caching datapoints for sensor with id: " + str(sensor_id))




