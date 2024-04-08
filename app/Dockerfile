# Dockerfile no diretório /app

# Use a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o contêiner
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Executa a aplicação
CMD ["python", "app.py"]
