import cv2

def resize(img, params):
	print 'Applying resize filter'
	width = params['width']
	height = params['height']
	return cv2.resize(img, (width, height), interpolation = cv2.INTER_CUBIC)

def crop(img, params):
	print 'Applying crop filter'
	x = params['x']
	y = params['y']
	w = params['w']
	h = params['h']
	return img[y:y+h, x:x+w]

def blur(img, params):
	print 'Applying blur filter'
	size = params['size']
	sigma = float(params['sigma'])
	return cv2.GaussianBlur(img, (size, size), sigma)

def grayscale(img, params):
	print 'Applying grayscale filter'
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def rotate(img, params):
	print 'Applying rotate filter'
	angle = params['angle']
	height, width = img.shape[:2]
	m = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
	return cv2.warpAffine(img, m, (width, height))

def flip(img, params):
	print 'Applying flip filter'
	mode = params['mode']
	return cv2.flip(img, mode)

def pyramid_up(img, params):
	print 'Applying pyramid up filter'
	return cv2.pyrUp(img)

def pyramid_down(img, params):
	print 'Applying pyramid down filter'
	return cv2.pyrDown(img)

def write_to_file(fileName, img):
	cv2.imwrite(fileName, img)