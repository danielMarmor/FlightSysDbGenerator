import pika
import json


class UpdateProgressConsumer:
    RESPONSE_QUEUE_NAME = 'FlightSysDbUpdateProgress'

    def __init__(self, update_progress_thread):
        self.update_progress_thread = update_progress_thread
        self.connection = None
        self.channel = None
        self.init_connection()

    def init_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_delete(self.RESPONSE_QUEUE_NAME)
        self.channel.queue_declare(queue=self.RESPONSE_QUEUE_NAME)

    def consume_update_progress(self):
        try:
            self.channel.basic_consume(queue=self.RESPONSE_QUEUE_NAME,
                                       on_message_callback=self.update_progress_callback,
                                       auto_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
            self.channel.queue_delete(self.RESPONSE_QUEUE_NAME)
            self.connection.close()
        except Exception as exc:
            self.channel.queue_delete(self.RESPONSE_QUEUE_NAME)
            self.connection.close()
            raise exc

    def update_progress_callback(self, ch, method, properties, body):
        message = json.loads(body)
        object_type = message['object_type']
        message_type = message['message_type']
        error_desc = message['error_desc']
        if message_type == 'OK':
            self.update_progress_thread.register_ok(object_type)
        elif message_type == 'ERROR':
            self.update_progress_thread.register_error(object_type, error_desc)
        elif message_type == 'COMPLETED':
            self.update_progress_thread.register_completed()



