from gcloud import datastore

CREDS_FILE = 'creds.json'
PROJECT = 'cloudcv-1302'

class Datastore:
	def __init__(self):
		self.client = datastore.Client.from_service_account_json(CREDS_FILE, project=PROJECT)

	def get(self, kind, id):
		key = self.client.key(kind, id)
		entity = self.client.get(key)
		return entity

	def put(self, entity):
		self.client.put(entity)