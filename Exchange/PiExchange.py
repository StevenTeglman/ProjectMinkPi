import sys
import pika

# Set up the exchange environment
credentials = pika.PlainCredentials('StevenTeglman', 'group13')
parameters = pika.ConnectionParameters('192.168.1.6', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

# Establish a queue called 'temp'
# TODO Change the exclusive based on whether or not we want the queues to be persistant.
result = channel.queue_declare(queue='', exclusive=False)
queue_name = result.method.queue

binding_keys = sys.argv[1:]

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)


for binding_key in binding_keys:
    channel.queue_bind(
        exchange='sensor_exchange', queue=queue_name, routing_key=binding_key)

print(' [*] PiExchange is waiting for messages. To exit press CTRL + C...')
