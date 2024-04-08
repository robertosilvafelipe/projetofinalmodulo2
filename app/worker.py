import pika # type: ignore
from redis import Redis # type: ignore

# Configurações do RabbitMQ
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'uploadQueue'

# Configurações do Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def process_file(file_name):
    # Aqui você poderia adicionar o código para redimensionar a imagem, se necessário.
    # Por exemplo: image.resize((800, 600), Image.ANTIALIAS)

    # Armazenar os metadados no Redis
    # Supondo que 'file_name' contém o nome do arquivo, 
    # você pode ajustar quais metadados salvar conforme necessário.
    redis_client.setex(file_name, 60, 'Uploaded')

def callback(ch, method, properties, body):
    file_name = body.decode()
    print(f"Received {file_name}")
    process_file(file_name)
    print(f"Processed {file_name}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
