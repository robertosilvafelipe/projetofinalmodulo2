from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import cgi
from minio import Minio # type: ignore
from minio.error import S3Error # type: ignore
import pika # type: ignore
import os

# Configurações do MinIO
# Substitua 'localhost' pelo nome do serviço MinIO definido no docker-compose.yml
MINIO_URL = 'minio:9000'
ACCESS_KEY = os.environ.get('MINIO_ROOT_USER', 'minioadmin')
SECRET_KEY = os.environ.get('MINIO_ROOT_PASSWORD', 'minioadmin')
BUCKET_NAME = 'meubucket'

# Configurações do RabbitMQ
# Substitua 'localhost' pelo nome do serviço RabbitMQ definido no docker-compose.yml
RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'uploadQueue'

minio_client = Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

def publish_message(file_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=f'File {file_name} uploaded',
        properties=pika.BasicProperties(
            delivery_mode=2,  # Faz a mensagem persistente
        )
    )
    connection.close()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']}
            )

            file_item = form['file']
            file_name = file_item.filename
            file_data = file_item.file

            try:
                if not minio_client.bucket_exists(BUCKET_NAME):
                    minio_client.make_bucket(BUCKET_NAME)
                
                #Determina o tamanho do arquivo  
                file_size = os.fstat(file_data.fileno()).st_size
                
                minio_client.put_object(
                BUCKET_NAME,
                file_name,
                file_data,
                length=file_size,  # Aqui você passa o tamanho do arquivo
                content_type='application/octet-stream'
            )

                # Enviar mensagem para a fila do RabbitMQ
                publish_message(file_name)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"File uploaded successfully to MinIO and message sent to RabbitMQ.")
            except (S3Error, pika.exceptions.AMQPError) as exc:
                self.send_response(500)
                self.end_headers()
                response = bytes(f"An error occurred: {exc}", 'utf-8')
                self.wfile.write(response)

# A porta deve ser a mesma que é exposta e mapeada no docker-compose.yml
PORT = 5000

handler = ServerHandler

with ThreadedHTTPServer(("", PORT), handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
