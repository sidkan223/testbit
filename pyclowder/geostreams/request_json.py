import requests
import json
import logging
import time


def get_json(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code==200:
                try:
                    return response.json()
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
    while True:
        try:
            response = requests.get(url)
            if response.status_code==200:
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
    headers = {'content-type': 'application/json'}
    count = 0
    while True:
        try:
            count+=1
            if count >6:
                return None
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning(" [pyG.request_json] ERROR: Could not POST data: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For url: " + str(url))
                logging.warning(" [pyG.request_json] and data: " + str(data))
                logging.warning(" [pyG.request_json] Waiting 4 seconds and will try again")
                time.sleep(4)
        except:
            logging.warning(" [pyG.request_json] ERROR POSTing for url: " + str(url))
            try:
                logging.warning(" [pyG.request_json] Response code: " + str(response.status_code))
            except:
                pass
            logging.warning(" [pyG.request_json] and data: " + str(data))
            logging.warning(" [pyG.request_json] Waiting 4 seconds and will try again")
            time.sleep(4)

def delete_datapoint(url):
    while True:
        try:
            response = requests.delete(url)
            if response.status_code==200:
                return response.json()
            else:
                logging.warning(" [pyG.request_json] ERROR: could not DELETE datapoint: [" + str(response.status_code) + "]")
                logging.warning(" [pyG.request_json] For URL: " + str(url))
                logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
                time.sleep(5)
        except:
            logging.warning(" [pyG.request_json] ERROR DELETEing for url: " + str(url))
            logging.warning(" [pyG.request_json] Waiting 5 seconds and will try again")
            time.sleep(5)


