FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar ficheiros de requisitos
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Descarregar modelo spaCy português (via pip para evitar problemas de URL)
RUN pip install https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.7.0/pt_core_news_sm-3.7.0-py3-none-any.whl

# Copiar código da aplicação
COPY app/ ./app/
COPY sample_texts/ ./sample_texts/

# Criar diretórios necessários
RUN mkdir -p uploads

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=app.web_app
ENV PYTHONUNBUFFERED=1

# Comando para executar a aplicação
CMD ["python", "-m", "app.web_app"]
