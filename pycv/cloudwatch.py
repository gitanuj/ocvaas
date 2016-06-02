import boto3

NAMESPACE = 'cloudy'

class CloudWatch:
	def __init__(self):
		self.client = boto3.client('cloudwatch')

	def publish_queue_length(self, length):
		self.client.put_metric_data(
		    Namespace=NAMESPACE,
		    MetricData=[
		        {
		            'MetricName': 'queue-length',
		            'Value': float(length),
		            'Unit': 'Count'
		        },
		    ]
		)
		print 'Published queue length ', length