# Projeto 

Projeto Final
O projeto final vai se basear no projeto do modulo anterior, mesmo as pessoas que não finalizaram o projeto passado poderão desenvolver utilizando o que foi feito.

O projeto se baseia na criação de um docker compose, com os seguintes serviços:

• Aplicação

• Minio

• Redis

• RabbitMQ

O docker compose deve conter uma orquestração dos container, onde a aplicação deve ser o ultimo container a subir, garantindo assim que quando subir a aplicação não encontre nenhum error.

• Volume para persistir os dados do container do Minio, Redis e Rabbit.
• Criação de uma network e expor apenas as portas necessárias.
• Criação de um dockerfile para a aplicação.

Pense que é uma aplicação que deve ter como preocupação uma alta disponibilidade e que seja resiliente.

A entrega pode ser feita através de um repositório como o GitHub. Deve conter:

• Uma documentação de como funciona o seu software
• Quais os comandos necessário para executar a solução
• Todos os arquivos: Lógica da aplicação, Dockerfile e um docker compose.
Lembre que toda solução deve esta contida no repositório , sem nenhuma ação previa no host que vai executar a solução .

----
# Descrição do funcionamento da aplicação 

O cliente deverá via interface gráfica enviar seus dados para realizar a transação. O arquivo de dados aceito deve estar no formato .json e deverá conter a seguinte estrutura:

```json
[{
    "_id": "cliente1",
    "isActive": true,
    "cliente": "Cliente fulano",
    "email": "clientefulanoo@example.com",
    "endereco": "Cidade A, Estado A, 1000",
    "datatrasancao": "2024-03-11T12:00:00 +00:00"
  }]
```

Ao enviar os dados, será enviado um evento para fila do rabbimq, criado uma chave no redis cache e também salvo os dados do cliente no minio.

----

# Estrutura da aplicação


```python
ProjetoFinalMod2/
|-- app/
|   |-- Dockerfile
|   |-- [app.py]
|   |-- requirements.txt
|   |-- index.html
|   |-- [worker.py]
|   |-- Dados.json
|   |-- Dados - Fraude1.json
|   ...
|-- nginx/
|   |-- Dockerfile
|   |-- nginx.conf
|-- docker-compose.yml
```




# Pull das imagens no docker HUB

docker pull robertosilvafelipe/projetofinalmod2-nginx:latest

docker push robertosilvafelipe/projetofinalmod2-app:latest


# Descrição do fluxo do projeto (sistema)

```scss
[Usuário] --> [NGINX] --> [Aplicação Web]
                     |
                     |--> [MinIO] (Armazenamento de Fotos)
                     |
                     |--> [RabbitMQ] (Fila de Processamento)
                               |
                               V
                       [Worker] (Processa Fotos e redimensiona)
                               |
                     |--> [Redis] (Armazenamento de Metadados)

```

Descrição do fluxo:
                     

1. **Usuário (com notebook)**: Interage com a aplicação web para envio dos dados da transação
2. **NGINX**: Atua como proxy reverso, direcionando as requisições para os serviços corretos.
3. **Aplicação Web**: Interface principal para os usuários enviarem os dados.
4. **MinIO**: Serviço de armazenamento de objetos onde os dados dos clientes são armazenados
5. **RabbitMQ**: Gerencia a fila de mensagens para o processamento das mensagens
6. **Worker**: Processa as mensagens de acordo com a chegada na fila do RabbitMQ.
7. **Redis**: Armazena dados dos clientes por 60s para


# Execução da aplicação 

Após realização do pull das imagens e build com o docker compose, abrir no navegador a url do ambiente na porta 8080.

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/ada27c0f-bd7b-4ccb-9363-6d62b26f18d9)


Realizar o envio das informações do cliente e clicar em "Enviar dados de Transação"

Deverá ser criado uma fila no rabbimq - (Rabbitmq é aberto na porta 15672)
Os dados deverão ser gravados no minio - (Minio é aberto na porta 9001)
E será criado uma key no redis para salvar informações básicas do cliente - (redis é aberto na porta 8001)


Minio 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/76f783c2-fc81-4b44-bbae-bac6825674a6)


Rabbit MQ 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/d8cffaac-5338-42ed-85c9-10aa16d09364)


Redis 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/94f5dcc3-7fd1-42d0-9f83-90f23d3b557e)
