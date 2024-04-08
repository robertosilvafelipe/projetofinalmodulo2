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

# Estrutura da aplicação


```python
ProjetoFinalMod2/
|-- app/
|   |-- Dockerfile
|   |-- [app.py]
|   |-- requirements.txt
|   |-- index.html
|   |-- [worker.py]
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
                     

1. **Usuário (com notebook)**: Interage com a aplicação web para upload e visualização de fotos.
2. **NGINX**: Atua como proxy reverso, direcionando as requisições para os serviços corretos.
3. **Aplicação Web**: Interface principal para os usuários interagirem com a galeria de fotos.
4. **MinIO**: Serviço de armazenamento de objetos onde as fotos são armazenadas.
5. **RabbitMQ**: Gerencia a fila de mensagens para o processamento de fotos
6. **Worker**: Processa as fotos de acordo com as mensagens na fila do RabbitMQ.
7. **Redis**: Armazena metadados das fotos para acesso rápido.


# Execução da aplicação 

Após realização do pull das imagens e build com o docker compose, abrir no navegador a url do ambiente na porta 8080.

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/6666b72a-c2c9-4011-bba3-c02e7f2d1560)

Realizar  o upload de uma imagem e clicar no upload.

Deverá ser criado uma fila no rabbimq - (Rabbitmq é aberto na porta 15672)
A imagem deverá ser gravada no minio - (Minio é aberto na porta 9001)
E será criado uma key no redis para salvar informações básicas da imagem - (redis é aberto na porta 8001)


Minio 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/76f783c2-fc81-4b44-bbae-bac6825674a6)


Rabbit MQ 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/d8cffaac-5338-42ed-85c9-10aa16d09364)


Redis 

![image](https://github.com/robertosilvafelipe/projetofinalmodulo2/assets/101230256/94f5dcc3-7fd1-42d0-9f83-90f23d3b557e)
