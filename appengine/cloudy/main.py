#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import pika
from datastore import Datastore
from gcloud import datastore

PROJECT = 'cloudcv-1302'
ENTITY_KIND = 'job'
QUEUE = 'queue'
AMQP_URL = ''
REQUEST_RECEIVED = 1

ds = Datastore()

def publish_msg(message):
    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = conn.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_publish(exchange='', routing_key=QUEUE, body=message, properties=pika.BasicProperties(delivery_mode=2))
    conn.close()

def format_entity(entity):
	data = json.loads(entity['data'])
	data['id'] = entity.key.id
	return json.dumps(data)

class GetHandler(webapp2.RequestHandler):
    def get(self, id):
    	entity = ds.get(ENTITY_KIND, long(id))
        self.response.write(format_entity(entity))

class PostHandler(webapp2.RequestHandler):
    def post(self):
    	entity = datastore.Entity(key=datastore.Key(ENTITY_KIND, project=PROJECT))
    	data = json.loads(self.request.body)
    	data['status'] = REQUEST_RECEIVED
    	entity['data'] = json.dumps(data)
    	ds.put(entity)
        publish_msg(str(entity.key.id))
    	self.response.write(format_entity(entity))

app = webapp2.WSGIApplication([
    ('/api/(\d+)', GetHandler),
    ('/api', PostHandler)
], debug=True)
