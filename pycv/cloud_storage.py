from gcloud import storage

CREDS_FILE = 'creds.json'
PROJECT = 'cloudcv-1302'
BUCKET_NAME = 'cloudy-bucket'

class CloudStorage:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(CREDS_FILE, project=PROJECT)
        self.bucket = self.client.get_bucket(BUCKET_NAME)

    def upload(self, filename):
        blob = self.bucket.blob(filename)
        blob.upload_from_filename(filename=filename)
        return blob.public_url