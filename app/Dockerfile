# Stage 1: Instalar dependencias en entorno aislado
FROM python:3.13-alpine AS builder

WORKDIR /install

# Instalar paquetes para compilar
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install-deps -r requirements.txt

# Stage 2: Imagen limpia
FROM python:3.13-alpine

WORKDIR /app

# Instalar biblioteca PostgreSQL
RUN apk add --no-cache libpq

# Copiar solo las dependencias ya instaladas desde builder
COPY --from=builder /install-deps /usr/local

# Copiar tu aplicación y estáticos
COPY app.py .
COPY /static/ static/

CMD ["python", "app.py"]
