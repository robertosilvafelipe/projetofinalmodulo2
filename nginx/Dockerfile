# Use a imagem oficial do NGINX
FROM nginx:alpine


# O comando COPY espera que nginx.conf esteja no mesmo diretório que este Dockerfile
COPY nginx.conf /etc/nginx/nginx.conf

# Copie os arquivos estáticos e o arquivo de configuração para o contêiner
#COPY app /usr/share/nginx/html

# Expõe a porta 80 para o proxy
EXPOSE 80

# Inicia o NGINX
CMD ["nginx", "-g", "daemon off;"]
