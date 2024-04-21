import pika
import redis
import os
import json
import time

# Configurações do RabbitMQ
RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'transactionQueue'

# Configurações do Redis
REDIS_HOST = 'redis'
REDIS_PORT = 6379
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def has_suspicious_address_change(new_address, old_address):
    # Verifica se o endereço completo mudou
    return new_address != old_address

def callback(ch, method, properties, body):
    transactions = json.loads(body)  # Supondo que seja uma lista de transações

    for transaction_data in transactions:
        transaction_id = transaction_data.get("_id")
        
        if transaction_id:
            # Obtém a última transação conhecida do Redis
            last_transaction_str = redis_client.get(transaction_id)
            if last_transaction_str:
                last_transaction = json.loads(last_transaction_str)
                # Verifica se o dado retornado do Redis é um dicionário
                if isinstance(last_transaction, dict):
                    old_address = last_transaction.get('endereco', '')
                    new_address = transaction_data.get('endereco', '')
                    if has_suspicious_address_change(new_address, old_address):
                        # Marca a transação como suspeita de fraude no Redis
                        redis_client.set(f"fraud_{transaction_id}", "true", ex=300)  # Expira em 5 minutos
                        print(f"Suspicious address change detected for transaction ID {transaction_id}: from {old_address} to {new_address}.")
                else:
                    print(f"The last transaction data for {transaction_id} is not a dictionary.")
            else:
                print(f"No last transaction data found for {transaction_id}.")

            # Atualiza a última transação conhecida no Redis
            redis_client.set(transaction_id, json.dumps(transaction_data), ex=60)  # Expira em 60 segundos

    # Reconhece a mensagem como processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            print('Consumer is running. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print("Connection failed, trying to reconnect in 5 seconds...", str(e))
            time.sleep(5)
        except KeyboardInterrupt:
            print('Consumer stopped.')
            break
        finally:
            try:
                connection.close()
            except:
                pass

if __name__ == '__main__':
    main()
