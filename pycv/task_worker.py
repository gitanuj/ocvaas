import cv2_utils
import utils
import os
import json
import uuid

EXECUTION_STARTED = 2
EXECUTION_FAILED = 3
EXECUTION_SUCCESSFUL = 4

def get_filter_func(filterType):
	switcher = {
		'resize'	: cv2_utils.resize,		# width, height
		'crop'		: cv2_utils.crop,		# x, y, w, h
		'blur'		: cv2_utils.blur,		# size, sigma
		'grayscale'	: cv2_utils.grayscale,
		'rotate'	: cv2_utils.rotate,		# angle
		'flip'		: cv2_utils.flip,		# mode
		'pyramid_up': cv2_utils.pyramid_up,
		'pyramid_down': cv2_utils.pyramid_down
	}
	return switcher.get(filterType)

class TaskWorker:
	def __init__(self, datastore, storage, entity):
		self.datastore = datastore
		self.storage = storage
		self.entity = entity
		self.job = json.loads(entity['data'])
		print 'Working on %s' % self.entity['data']

	def update_status(self, status):
		self.job['status'] = status
		self.entity['data'] = json.dumps(self.job)
		self.datastore.put(self.entity)
		print 'Updated to %s' % self.entity['data']

	def do_work(self):
		img = utils.url_to_image(self.job['src'])
		print 'Fetched image from %s' % self.job['src']

		res = img
		for f in self.job['filters']:
			func = get_filter_func(f['type'])
			params = f['params'] if 'params' in f else None
			res = func(res, params)

		filename = str(uuid.uuid4()) + '.jpg'
		cv2_utils.write_to_file(filename, res)

		url = self.storage.upload(filename)
		self.job['res'] = url
		print 'Uploaded result at %s' % url

		os.remove(filename)

	def start(self):
		self.update_status(EXECUTION_STARTED)
		try:
			self.do_work()
		except Exception as e:
			print 'Error occurred: %s' % e
		finally:
			if 'res' in self.job:
				self.update_status(EXECUTION_SUCCESSFUL)
			else:
				self.update_status(EXECUTION_FAILED)