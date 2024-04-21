from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
from minio import Minio
from minio.error import S3Error
import pika
import redis
import os
from io import BytesIO

# Configurações do MinIO
MINIO_URL = 'minio:9000'
ACCESS_KEY = os.environ.get('MINIO_ROOT_USER', 'minioadmin')
SECRET_KEY = os.environ.get('MINIO_ROOT_PASSWORD', 'minioadmin')
BUCKET_NAME = 'bucket-dadoscliente'

# Configurações do RabbitMQ
RABBITMQ_HOST = 'rabbitmq'
TRANSACTION_QUEUE_NAME = 'transactionQueue'

# Configuração do cliente Redis
REDIS_HOST = 'redis'
REDIS_PORT = 6379
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Cliente MinIO
minio_client = Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

def publish_to_queue(queue_name, data):
    """Publish messages to RabbitMQ."""
    try:
        with pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST)) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=data,
                properties=pika.BasicProperties(delivery_mode=2)
            )
    except Exception as e:
        print(f"Failed to publish message: {str(e)}")

def save_to_minio(data_bytes, file_name):
    """Save bytes data to MinIO as a file-like object."""
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
        
        data_stream = BytesIO(data_bytes)
        minio_client.put_object(
            BUCKET_NAME,
            file_name,
            data_stream,
            length=len(data_bytes),
            content_type='application/json'
        )
        data_stream.close()
    except Exception as e:
        print(f"Failed to save to MinIO: {str(e)}")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/check-fraud'):
            self.handle_check_fraud()
        elif self.path == '/':
            self.path = '/index.html'
            self.handle_file_request()

    def handle_file_request(self):
        try:
            with open(self.path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')

    def handle_check_fraud(self):
        transaction_id = self.path.split('?')[1].split('=')[1]
        is_fraud = redis_client.get(f"fraud_{transaction_id}") is not None
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'isFraud': is_fraud}).encode('utf-8'))

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        if self.path == '/upload':
            pass
        elif self.path == '/upload-json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            transaction_data = json.loads(post_data.decode('utf-8'))
            transaction_data_str = json.dumps(transaction_data)
            publish_to_queue(TRANSACTION_QUEUE_NAME, transaction_data_str)

            for transaction in transaction_data:
                transaction_id = transaction.get("_id", None)
                if transaction_id:
                    redis_client.setex(transaction_id, 60, transaction_data_str)
                    try:
                        save_to_minio(bytes(transaction_data_str, 'utf-8'), f"{transaction_id}.json")
                    except S3Error as exc:
                        print(f"An error occurred while saving to MinIO: {exc}")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'message': 'Transaction data received and processed'}).encode('utf-8')
            self.wfile.write(response)

if __name__ == "__main__":
    PORT = 5000
    server = ThreadedHTTPServer(('', PORT), ServerHandler)
    print(f"Serving at port {PORT}")
    server.serve_forever()
