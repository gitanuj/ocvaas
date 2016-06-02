from task_worker import TaskWorker
from datastore import Datastore
from cloud_storage import CloudStorage
from cloudwatch import CloudWatch
import threading
import pika

ENTITY_KIND = 'job'
QUEUE = 'queue'
AMQP_URL = ''

DATASTORE = Datastore()
STORAGE = CloudStorage()
CLOUDWATCH = CloudWatch()

def publish_queue_length(channel):
	try:
		count = channel.queue_declare(queue=QUEUE, durable=True).method.message_count
		CLOUDWATCH.publish_queue_length(count)
	finally:
		threading.Timer(5, publish_queue_length, [channel]).start()

def callback(ch, method, properties, body):
	try:
		entity = DATASTORE.get(ENTITY_KIND, long(body))
		worker = TaskWorker(DATASTORE, STORAGE, entity)
		worker.start()
	finally:
		ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
	connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
	channel = connection.channel()
	publish_queue_length(channel)
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue=QUEUE)

	print 'Listening for jobs...'
	channel.start_consuming()

if __name__ == '__main__':
	main()