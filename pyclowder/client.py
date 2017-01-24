"""
    ClowderClient
    ~~~
    This module contains a basic client to interact with the Clowder API.
"""

import requests
import logging
import json


class ClowderClient(object):
    """
    Client to Clowder API to store connection information.

    The `path` parameter used by many of the methods in this class call a specific path relative to the host + "api".
    For example passing in "/version" for host "https://seagrant-dev.ncsa.illinois.edu/clowder/" will call
    "https://seagrant-dev.ncsa.illinois.edu/clowder/api/version".
    """
    logger = logging.getLogger(__name__)
    api_fragment = "/api"
    max_retries = 10
    call_timeout = 5
    headers = {'content-type': 'application/json'}

    def __init__(self, *args, **kwargs):
        """
        Create an instance of `ClowderClient`.

        :param string host: The root host url of the specific geostreaming API we are connecting to.
        :param string key: The API key used to write to the API. Set this or `username`/`password` below.
        :param string username: HTTP Basic Authentication username. Set this or `key`.
        :param string password: HTTP Basic Authentication password. Set this or `key`.
         """
        self.host = kwargs.get('host')
        self.key = kwargs.get('key')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    def version(self):
        """Return Clowder version info."""
        url = self.host + self.api_fragment + "/version"
        self.logger.debug("GET %s", url)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            try:
                json = r.json()
                self.logger.debug("Version: %s", json)
                return json
            except ValueError:
                self.logger.error("GET %s. Could not parse JSON. Status %s.", url, r.status_code)
                r.raise_for_status()
        else:
            r.raise_for_status()

    def get_json(self, path):
        """
        Call HTTP GET against `path`. This version returns a JSON object.


        :param path: Endpoint path relative to Clowder api.
        :return: JSON-encoded content of the response.
        :raises: `requests.HTTPError`
        """
        url = self.host + self.api_fragment + path
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def get(self, path):
        """
        Call HTTP GET against `path`. This version returns a `requests.Response` object.

        :param path: Endpoint path relative to Clowder api.
        :return: `requests.Response` so that we can check status on it and then retrieve the JSON content of the response.
        :raises: `requests.HTTPError`
        """
        url = self.host + self.api_fragment + path
        try:
            return requests.get(url)
        except Exception as e:
            self.logger.error("GET %s: %s", url, e.message)

    def post(self, path, content):
        url = self.host + self.api_fragment + path
        try:
            return requests.post(url, data=json.dumps(content), headers=self.headers)
        except Exception as e:
            self.logger.error("GET %s: %s", url, e.message)




