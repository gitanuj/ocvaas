# CloudCV


OpenCV as a Service.
An on-demand Image Manipulation Service


# Demo

The app can be accesssed in the following [URL](http://client.cloudcv.ml/).
Upon hitting this URL, the user can:
1. GET the status of a job he previously submitted
2. Add/Submit a new job to manipulate an image. A new job to be submitted should be given as a JSON with the following  format:
```
		{
	       "filters":[
	            {
		            "type": "<filter1_name>", 
		            "params":{
		            	"<key1>":"<value1>", 
		            	"<key2>":"<value2>", 
		            }
		        },
		        {
		            "type": "<filter2_name>", 
		            "params":{
		            	"<key1>":"<value1>", 
		            	"<key2>":"<value2>", 
		            }
		        }
	       ],
	       "src":"<original_img_URL>"
	    }
```

# Allowed filters

1. 	Resize: Sample JSON for resizing the image is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "resize",
			"params": {
				"width": 200,
				"height": 200
			}
		}]
	}
```
2.	blur: Sample JSON for blurring the image is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type":"blur",
			"params": {
				"size": 5,
				"sigma": 5
			}
		}]
	}
```
3.	grayscale: Sample JSON for greying the image is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "grayscale"
		}]
	}
```
4.	rotate: Sample JSON for rotating the image is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "rotate",
			"params": {
				"angle": 45
			}
		}]
	}
```
5. flip: Sample JSON for flipping the image is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "flip",
			"params": {
				"mode": 1
			}
		}]
	}
```
6. pyramid_up: Sample json is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "pyramid_up"
		}]
	}
```
7. pyramid_up: Sample json is:
```
	{
		"src":"<original_img_URL>",
		"filters":[
		{
			"type": "pyramid_down"
		}]
	}
```

# Trying CloudCV APIs:

This app allows the following HTTP methods:
* GET
* POST

For using the service from a REST client the sample request is mentioned below:
* GET job: `http://client.cloudcv.ml/api/<job_id>`
	Sample JSON response is:
```
	{
	   "status":4,
	   "src":"http://www.name-list.net/img/portrait/Lenna_6.jpg",
	   "id":5103363892969472,
	   "filters":[
	      {
	         "type":"grayscale"
	      },
	      {
	         "params":{
	            "angle":45
	         },
	         "type":"rotate"
	      }
	   ],
	   "res":"https://storage.googleapis.com/cloudy-bucket/e262a770-08cb-4330-8b79-0ded4a8fecd9.jpg"
	}
```
* POST new job: `http://client.cloudcv.ml/api`
	- A new job to be submitted should be given as a JSON with the following format:
```
		{
	       "filters":[
	            {
		            "type": "<filter1_name>", 
		            "params":{
		            	"<key1>":"<value1>", 
		            	"<key2>":"<value2>", 
		            }
		        },
		        {
		            "type": "<filter2_name>", 
		            "params":{
		            	"<key1>":"<value1>", 
		            	"<key2>":"<value2>", 
		            }
		        }
	       ],
	       "src":"<original_img_URL>"
	    }
```
	- A sample JSON for POST is provided as follows:
```
		{
		   "filters":[
		        {"type": "grayscale"},
		        {"type": "rotate", "params": {"angle": 45}}
		   ],
		   "src":"http://www.name-list.net/img/portrait/Lenna_6.jpg"
		}
```

# Status Codes
 
The following is the mapping between the status codes and their usage in GET response from the API
- REQUEST_SUBMITTED = 1
- EXECUTION_STARTED = 2
- EXECUTION_FAILED = 3
- EXECUTION_SUCCESSFUL = 4

# Code Structure

- /appengine: 	This directory has all the Google AppEngine related code written in python
- /pycv:			This directory contains all the code related to the backend OpenCV workers that run on Docker instances
- /test: 			This directory contains the funk tests to generate load on our application
- Dockerfile:	This file contains the scripts that need to be run while launching the Docker instances.
- AppScalefile:	This file contains the script used to deploy our application intended orginally for Google App engine on 
				different cloud vendors such as AWS and Google Compute Engine.
				