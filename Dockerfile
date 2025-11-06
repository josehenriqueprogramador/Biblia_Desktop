# Usa imagem leve do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia tudo para o contêiner
COPY . .

# Instala dependências (se houver arquivo requirements.txt)
RUN pip install --no-cache-dir flask fastapi uvicorn jinja2

# Expõe a porta padrão do Render
EXPOSE 10000

# Comando para iniciar o servidor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
