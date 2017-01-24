import json
import logging
import time

import requests


def get_json(url):
    """POST JSON for url. If status is not 200, sleep for 5 seconds and retry. """
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    return response.json()
                # FIXME delete? not sure we want to accept non json response
                except:
                    return response.text
            else:
                logging.warning(" [pyG.request_json] ERROR: could not GET json: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For URL: " + str(url))
                logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
                time.sleep(5)
        except:
            logging.warning(" [pyG.request_json] ERROR GETting for url: " + str(url))
            logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
            time.sleep(5)


def get_rdb(url):
    # FIXME How is this different from the one above?
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                logging.warning(" [pyG.request_json] ERROR: could not GET json: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For URL: " + str(url))
                logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
                time.sleep(5)
        except:
            logging.warning(" [pyG.request_json] ERROR GETting for url: " + str(url))
            logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
            time.sleep(5)


def post_json(url, data):
    """POST JSON for url. If status is not 200, sleep for 5 seconds and retry. """
    headers = {'content-type': 'application/json'}
    count = 0
    while True:
        try:
            # FIXME why a max count here and not in the get_json above?
            count += 1
            if count > 6:
                return None
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning(" [pyG.request_json] ERROR: Could not POST data: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For url: " + str(url))
                logging.warning(" [pyG.request_json] and data: " + str(data))
                logging.warning(" [pyG.request_json] Waiting 4 seconds and will try again")
                # FIXME why 4 and not 5?
                time.sleep(4)
        except:
            logging.warning(" [pyG.request_json] ERROR POSTing for url: " + str(url))
            try:
                logging.warning(" [pyG.request_json] Response code: " + str(response.status_code))
            except:
                pass
            logging.warning(" [pyG.request_json] and data: " + str(data))
            logging.warning(" [pyG.request_json] Waiting 4 seconds and will try again")
            # FIXME why 4 and not 5?
            time.sleep(4)


def delete_datapoint(url):
    """Delete a data point. This does not update the cache."""
    while True:
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning(
                    " [pyG.request_json] ERROR: could not DELETE datapoint: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For URL: " + str(url))
                logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
                time.sleep(5)
        except:
            logging.warning(" [pyG.request_json] ERROR DELETEing for url: " + str(url))
            logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
            time.sleep(5)
