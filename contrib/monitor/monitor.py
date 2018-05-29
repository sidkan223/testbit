#!/usr/bin/env python

import datetime
import hashlib
import http.server
import json
import logging
import os
import threading
import sys

import pika

rabbitmq_uri = os.getenv('RABBITMQ_URI', 'amqp://guest:guest@localhost/%2F')

extractors = {}

hostName = ""
hostPort = 9999


class MyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(extractors), 'utf-8'))


def http_server():
    server = http.server.HTTPServer((hostName, hostPort), MyServer)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def callback(ch, method, properties, body):
    data = json.loads(body)
    data['updated'] = datetime.datetime.now().isoformat()
    if 'id' not in data and 'extractor_info' not in data and 'queue' not in data:
        print("BAD DATA : %r " % body)
        return

    extractor_info = data['extractor_info']

    if extractor_info['name'] not in extractors:
        extractors[extractor_info['name']] = {}

    if extractor_info['version'] not in extractors[extractor_info['name']]:
        extractors[extractor_info['name']][extractor_info['version']] = {
            'extractor_info': extractor_info,
            'queue': data['queue'],
            'extractors': {}
        }
    extractor = extractors[extractor_info['name']][extractor_info['version']]

    extractor['extractors'][data['id']] = {
        'last_seen': datetime.datetime.now().isoformat()
    }

    if extractor['queue'] != data['queue']:
        print("ERROR : mismatched queue names %s != %s." % (data['queue'], extractor['queue']))
        extractor['queue'] = data['queue']
    print(json.dumps(extractors))

def extractors_monitor():
    parameters = pika.URLParameters(rabbitmq_uri)
    connection = pika.BlockingConnection(parameters)

    # connect to channel
    channel = connection.channel()

    # create extractors exchange for fanout
    channel.exchange_declare(exchange='extractors', exchange_type='fanout', durable=True)

    # create anonymous queue
    result = channel.queue_declare(exclusive=True)
    channel.queue_bind(exchange='extractors', queue=result.method.queue)

    # listen for messages
    channel.basic_consume(callback, queue=result.method.queue, no_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    thread = threading.Thread(target=http_server)
    thread.setDaemon(True)
    thread.start()
    extractors_monitor()
