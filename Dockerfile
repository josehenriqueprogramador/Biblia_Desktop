# Usa imagem leve do Python
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala Flask e dependências
RUN pip install --no-cache-dir flask jinja2

# Exponha a porta exigida pelo Render
EXPOSE 10000

# Comando para rodar o Flask
CMD ["python", "app.py"]
