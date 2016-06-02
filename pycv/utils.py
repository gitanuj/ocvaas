import numpy as np
import urllib
import cv2

def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	return cv2.imdecode(image, cv2.IMREAD_COLOR)