# docker/app/Dockerfile
FROM python:3.12-slim

# Evita criar .pyc e garante logs sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Dependências de sistema (psycopg2 não é necessário se usar asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -m appuser

# Copia requirements primeiro para aproveitar cache
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# (Opcional) dependências de teste
ARG INSTALL_DEV=false
COPY requirements-dev.txt /app/requirements-dev.txt
RUN if [ "$INSTALL_DEV" = "true" ] && [ -f /app/requirements-dev.txt ]; then \
      pip install --no-cache-dir -r /app/requirements-dev.txt; \
    fi
    

# Copia o código da aplicação
COPY app /app/app

# Copia o código da aplicação de testes
COPY tests /app/tests

# Ajusta permissões
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Produção: sem --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
