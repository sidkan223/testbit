import logging
from datetime import datetime
from pytz import timezone, utc

# CONVERT TO UTC FORMAT            FROM EXAMPLE FORMAT 2015-11-20 03:46:20
def time2utc(date_in, time_zone="America/Chicago"):

    date_out = timezone(time_zone).localize(datetime.strptime(date_in,"%Y-%m-%d %H:%M:%S")).astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return date_out

def time_transform(timeStr, timeZn):
    output = ""
    if timeZn == "CDT":
        output = timeStr + ":00-05:00"
    elif timeZn == "CST":
        output = timeStr + ":00-06:00"
    elif timeZn == "EST":
        output = timeStr + ":00-05:00"
    elif timeZn == "EDT":
        output = timeStr + ":00-04:00"
    else:
        logging.warning("ERROR: timezone '" + timeZn + "' is not in the transform table")
        exit()

    output = output.replace(' ', 'T')
    return output