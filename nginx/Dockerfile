# Use a imagem oficial do NGINX
FROM nginx:alpine

# Instala o curl para checar a disponibilidade do serviço fraud_detection
RUN apk --no-cache add curl

# Copia o nginx.conf para o diretório correto
COPY nginx.conf /etc/nginx/nginx.conf

# Expõe a porta 80 para o proxy
EXPOSE 80

# Define o ENTRYPOINT que checa a disponibilidade do serviço fraud_detection
ENTRYPOINT ["sh", "-c", "until curl --output /dev/null --silent --head --fail http://fraud_detection:5000; do printf '.'; sleep 5; done; exec nginx -g 'daemon off;'"]

