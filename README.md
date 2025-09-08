# Práctica final - Contenedores: más que VMs - Docker
**XII Edición Bootcamp DevOps & Cloud Computing Full Stack**

**Evaristo García Zambrana | 3 de agosto de 2025**

---

[🔽 Ir directamente a Cómo desplegar kc-visit-count 🔽](https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker/blob/main/README.md#-c%C3%B3mo-desplegar-kc-visit-counter)

## Diagrama de arquitectura
Diagrama que contempla el resultado final de la arquitectura de microservicios desplegada por el *docker-compose.yml* de este repositorio.
![Diagrama de arquitectura de la aplicación desplegada con Docker Compose](https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker/blob/main/02%20-%20Diagrama%20Docker%20Compose%20-%20Evaristo%20GZ.drawio.jpg)

## Descripción de la aplicación

*kc-visit-counter* es una aplicación web desplegada en arquitectura de microservicios con Docker Compose. Desarrollada en Python y PostgreSQL, permite registrar cada visita HTTP y guarda fecha/hora en una base de datos PostgreSQL. Además, devuelve las 10 últimas visitas con fecha y hora.

- **Frontend**: Nginx como proxy inverso.
- **Backend**: Python 3.13 + Flask proporcionando directamente el HTML. Aloja los logs de Python en un volumen persistente de Docker.
- **Base de datos**: PostgreSQL 15 alojando los datos en un volumen persistente de Docker. Aloja los logs de PostgreSQL en un volumen persistente de Docker.
- **Logging**: Filebeat leyendo los logs de los volúmenes, pasándolo a Elasticsearch y visualizándolos a través de Kibana mediante un navegador web.
- **Orquestación**: Docker Compose, sirviendo como orquestador de servicios Docker.
- **Administrador de contenedores**: Portainer para la visualización y administración del stack a través de navegador web.

## Requisitos

- Docker Engine (o Docker Desktop).
- Docker Compose.
- Git.

Ejecutado en Windows 11 con Docker Desktop 4.43.2, Docker Engine 28.3.2, Docker Compose v2.38.2-desktop.1 mediante WSL 2.

## Estructura del repositorio
```
├── app                               <--- Directorio para el contenido del servicio Python.
│   ├── Dockerfile                    <--- Dockerfile para el contenedor de Python.
│   ├── Dockerfile_sin_multistage     <--- Dockerfile sin la tarea de multistage.
│   ├── app.py                        <--- Código Python + Flask de la app.
│   ├── requirements.txt              <--- Archivo requirements.
│   └── static                        <--- Directorio para los estáticos de la app.
│       └── style.css                 <--- Hoja de estilo aplicada al HTML de la app.
├── docker-compose.yml                <--- docker-compose.yml del entorno de producción.
├── docker-compose_test.yml           <--- docker-compose_test.yml del entorno de test.
├── filebeat                          <--- Directorio para el contenido del servicio Filebeat.
│   ├── filebeat.yml                  <--- Fichero de configuración de Filebeat.
├── nginx                             <--- Directorio para el contenido del servicio Nginx.
│   └── nginx.conf                    <--- Fichero de configuración de Nginx.
└── postgresql                        <--- Directorio para el contenido del servicio db.
    ├── Dockerfile                    <--- Dockerfile para el contenedor de PostgreSQL.
    ├── init-scripts                  <--- Directorio para los entrypoints del contenedor.
    │   ├── 01-schema.sql             <--- Fichero de creación de tablas de la base de datos.
    │   └── 02-users.sh               <--- Fichero de creación de usuarios de la base de datos.
    └── postgresql.conf               <--- Fichero de configuración de PostgreSQL.
```

---

## 🚀 Cómo desplegar kc-visit-counter

### 1. Clona el repositorio de GitHub
```
git clone https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker
```


### 2. Ubícate en el directorio Git
```
cd EvaristoGZ_02-Docker
```

### 3. Da permisos a filebeat.yml
En algunos sistemas operativos, es necesario dar permisos al fichero de configuración de Filebeat para que el contenedor arranque.
Ejecuta:
```
chmod 644 filebeat/filebeat.yml
```

### 4. Crea el fichero .env
Crea un fichero .env con el siguiente contenido:
```
# Aprovisionamiento PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SUPER-PA$$WORD
POSTGRES_DB=kc-visit-counter

# Cadena conexión BBDD
DB_NAME=kc-visit-counter
DB_USER=kc-user
DB_PASSWORD=kc-PA$$WORD
DB_HOST=db
DB_PORT=5432

# Otros
TZ=Europe/Madrid
```


### 5. Levanta el Docker Compose
Este paso, además, construirá las imágenes de Docker y las descargará en caso de ser necesario. Creará los servicios, contenedores, redes y volúmenes.
```
docker compose up --build -d
```

Puedes usar `docker compose --build` para que se muestre la salida de los logs de contenedores en pantalla.


### 6. Verifica el estado del Compose
Ejecutamos `docker compose ls` para conocer el estado del compose.

En la columna status deberá poner *running(7)*.


### 7. Accede al servicio web
A través de un navegador web, accede a [http://localhost](http://localhost)

El resultado esperado es un número, que representa el total de las visitas o peticiones a esa dirección URL y una tabla con las últimas 10 visitas.

### 8. Comprueba el acceso al resto de servicios
- **Portainer**
  
  Será el primero, puesto que dispone de un máximo de 5 minutos para establecer la contraseña de admin.

  Accedemos a través de un navegador web a [http://localhost:9000](http://localhost:9000)

- **Kibana**
  
  Accedemos a través de un navegador web a [http://localhost:5601](http://localhost:5601)

  La primera vez que iniciamos Kibana tenemos que crear el Data View:

  1. Accedemos en el menú lateral a  Analytics>Discover.
     - Name: filebeat-*
     - Index pattern: filebeat-*
  3. A la derecha aparecerá los índices que coinciden con el patrón.
  4. Pulsamos sobre el botón “Save data view to Kibana”.
  5. Visualizamos los datos y realizamos nuevas peticiones a la app web si deseamos.


### 9. Para el Docker Compose
Tras realizar las comprobaciones de los servicios y comprobar el funcionamiento de la infraestructura, el penúltimo paso es parar el Docker Compose.

Ubicados en el directorio del repositorio ejecutamos:
```
docker compose down
```
Esto eliminará los servicios, los contenedores y las redes. En caso de querer volver a ejecutarlos, basta con ejecutar `docker compose up -d`

### 10. Elimina los servicios creados con Docker Compose
Por último, si deseas no tener rastro de este proyecto en tu sistema, utiliza el parámetro *-d*:
```
docker compose down -v
```

Esto hará que, además de parar los servicios, contenedores y redes, elimine también volúmenes creados por el fichero *docker-compose.yml*.

Recuerda que, la eliminación de los volúmenes no es una eliminación del recurso virtual, si no que también conlleva la eliminación de los datos alojados en él. Estos no se alojan en ningún otro lugar y no serán recuperables.

---

## Documento paso a paso
Este repositorio forma parte de la Práctica Final del módulo "Contenedores: más que VMs - Docker" perteneciente a la XII Edición Bootcamp DevOps & Cloud Computing Full Stack.

Puedes consultar los hitos principales y los hitos extras que se solicitaban en el documento PDF: "[01 - Evaristo GZ - Práctica Final Contenedores, más que VMs - Docker.pdf](https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker/blob/main/01%20-%20Evaristo%20GZ%20-%20Pr%C3%A1ctica%20Final%20-%20Contenedores%2C%20m%C3%A1s%20que%20VMs%20-%20Docker.pdf)" donde se detalla y explica el paso a paso para completar los requerimientos.


## Errores comunes
### docker compose ls muestra running(6) en vez de running(7)
Claramente, falta un servicio por iniciar. Ejecuta `docker compose ps` para ver qué servicios están corriendo.

Identifica el servicio que no está actualmente levantado y ejecuta `docker logs NombreContenedor` para ver los logs de éste.

### El contenedor filebeat-kc-vc no está corriendo
Si tras el punto anterior, encuentras que el contenedor *filebeat-kc-vc* no está corriendo, es posible que sea debido a que el fichero *filebeat.yml* no tiene permisos correctos. Comprueba que, la salida de `docker logs filebeat-kc-vc` sea algo parecido a esto:
```
Exiting: error loading config file: config file ("filebeat.yml") can only be writable by the owner but the permissions are "-rw-rw-r--" (to fix the permissions use: 'chmod go-w /usr/share/filebeat/filebeat.yml')
```

En caso de ser así, ejecuta el [paso 3 de Cómo desplegar kc-visit-count](https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker?tab=readme-ov-file#3-da-permisos-a-filebeatyml) y vuelve a intentar levantar el Docker Compose.

### .env not found
Si recibes este error, significa que no has creado el .env detallado en el [paso 4 de Cómo desplegar kc-visit-count](https://github.com/KeepCodingCloudDevops12/EvaristoGZ_02-Docker?tab=readme-ov-file#4-crea-el-fichero-env) o bien lo has creado en otro directorio distinto al directorio del repositorio.

### No puedo acceder a Portainer
Portainer tiene una medida de seguridad que impide establecer una contraseña para el usuario admin si han pasado más de cinco minutos y nadie ha accedido a la dirección URL.

El mensaje es algo parecido a:
```
Your Portainer instance timed out for security purposes. To re-enable your Portainer instance, you will need to restart Portainer.
```

Si esto ocurre, no es necesario parar y volver a arrancar todo el compose. Simplemente ejecuta `docker restart portainer-kc-vc` y vuelve a acceder a la dirección URL de Portainer.

