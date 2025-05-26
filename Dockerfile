FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para o banco de dados SQLite
RUN mkdir -p instance

# Variáveis de ambiente para produção
ENV FLASK_APP=src.main
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main:app"]
