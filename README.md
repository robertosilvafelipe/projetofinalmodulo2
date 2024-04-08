# Projeto 

Projeto Final
O projeto final vai se basear no projeto do modulo anterior, mesmo as pessoas que não finalizaram o projeto passado poderão desenvolver utilizando o que foi feito.

O projeto se baseia na criação de um docker compose, com os seguintes serviços:

• Aplicação
• Minio
• Redis
• RabbitMQ
O ocker compose deve conter uma orquestração dos container, onde a aplicação deve ser o ultimo container a subir, garantindo assim que quando subir a aplicação não encontre nenhum error.

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

Estrutura da aplicação

|-- app/
|   |-- Dockerfile
|   |-- app.py
|   |-- requirements.txt
|   |-- index.html
|   |-- worker.py
|   ...
|-- nginx/
|   |-- Dockerfile
|   |-- nginx.conf
|-- docker-compose.yml



Pull das imagens no docker HUB

docker pull robertosilvafelipe/projetofinalmod2-nginx:latest

docker push robertosilvafelipe/projetofinalmod2-app:latest


Descrição do fluxo do projeto (sistema)

Descrição do fluxo:

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

1. **Usuário (com notebook)**: Interage com a aplicação web para upload e visualização de fotos.
2. **NGINX**: Atua como proxy reverso, direcionando as requisições para os serviços corretos.
3. **Aplicação Web**: Interface principal para os usuários interagirem com a galeria de fotos.
4. **MinIO**: Serviço de armazenamento de objetos onde as fotos são armazenadas.
5. **RabbitMQ**: Gerencia a fila de mensagens para o processamento de fotos
6. **Worker**: Processa as fotos de acordo com as mensagens na fila do RabbitMQ.
7. **Redis**: Armazena metadados das fotos para acesso rápido.

