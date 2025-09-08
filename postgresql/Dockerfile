FROM postgres:15

# Copiar archivo de configuración
COPY postgresql.conf /etc/postgresql/postgresql.conf

# Crear y dar permisos a carpeta logs
RUN mkdir -p /var/log/postgresql \
    && chown postgres:postgres /var/log/postgresql

# Copiar scripts de inicialización
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Usar el nuevo archivo postgresql.conf
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
