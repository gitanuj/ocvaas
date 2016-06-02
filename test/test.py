import random
import json
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def payload(url):
	p = dict()
	p['src'] = url
	p['filters'] = [
		{
			'type': 'blur',
			'params': {
				'size': 5,
				'sigma': 5
			}
		},
		{
			'type': 'rotate',
			'params': {
				'angle': 45
			}
		},
		{
			'type': 'flip',
			'params': {
				'mode': 1
			}
		}
	]
	return json.dumps(p)

class Cloudy(FunkLoadTestCase):
	def setUp(self):
		self.server_url = self.conf_get('main', 'url')

	def test_simple(self):
		server_url = self.server_url
		nb_time = self.conf_getInt('test_cloudy', 'nb_time')
		for i in range(nb_time):
			p = payload(random_line(open('urls.txt')))
			self.post(self.server_url, params=Data('application/json', p), description="post job api")
			status = json.loads(self.getBody())['status']
			self.assert_(status == 1)

if __name__ in ('main', '__main__'):
    unittest.main()