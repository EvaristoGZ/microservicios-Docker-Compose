from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import psycopg2
from datetime import datetime
import os
import time
import logging
from pythonjsonlogger import jsonlogger

# === Configuración del logger en JSON ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Formateador JSON
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')

# Handler para consola (stdout)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Guardar en archivo log
try:
    os.makedirs("/var/log/kc-visit-counter", exist_ok=True)
    file_handler = logging.FileHandler('/var/log/kc-visit-counter/app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning("No se pudo inicializar logging en archivo: /var/log/kc-visit-counter/app.log", exc_info=e)


# === Flask App ===
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# Configuración DB desde variables de entorno
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "basedatos"),
    "user": os.environ.get("DB_USER", "usuario"),
    "password": os.environ.get("DB_PASSWORD", "contrasenya"),
    "host": os.environ.get("DB_HOST", "db"),
    "port": os.environ.get("DB_PORT", "5432")
}
logger.info("Configuración de conexión", extra=DB_CONFIG)

# Reintento de conexión
max_retries = 10
for i in range(max_retries):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("✅ Conexión con PostgreSQL establecida.")
        break
    except psycopg2.OperationalError as e:
        logger.warning(f"⏳ Esperando PostgreSQL... ({i+1}/{max_retries})", exc_info=e)
        time.sleep(2)
else:
    logger.critical("❌ PostgreSQL no responde tras varios intentos.")
    raise Exception("❌ PostgreSQL no responde.")

cursor = conn.cursor()

@app.route("/")
def registrar_y_mostrar():
    try:
        fecha_hora = datetime.now()
        cursor.execute("INSERT INTO visitas (fecha_hora) VALUES (%s)", (fecha_hora,))
        conn.commit()

        # Total visitas
        cursor.execute("SELECT COUNT(*) FROM visitas")
        total_visitas = cursor.fetchone()[0]

        # Últimas 10 visitas
        cursor.execute("SELECT id, fecha_hora FROM visitas ORDER BY id DESC LIMIT 10")
        visitas = cursor.fetchall()

        # Renderizado HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
            <meta charset="UTF-8">
            <title>App kc-visit-counter | Evaristo GZ</title>
        </head>
        <body>
            <center>
                <h1>Total de visitas<br><span id="numero">{total_visitas}</span></h1>
                <h2>Últimas visitas</h2>
                <table border="1" cellpadding="8" cellspacing="0">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Fecha y hora</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for v in visitas:
            html += f"<tr><td>{v[0]}</td><td>{v[1].strftime('%d/%m/%Y %H:%M:%S')}</td></tr>"

        html += """
                    </tbody>
                </table>
            </center>
        </body>
        </html>
        """
        return html

    except Exception as e:
        logger.error("❌ Error al manejar la solicitud principal", exc_info=e)
        return "Error interno del servidor", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

