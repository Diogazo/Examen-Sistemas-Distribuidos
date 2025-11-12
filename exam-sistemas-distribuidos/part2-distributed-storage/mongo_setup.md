# Configuración del Almacenamiento Distribuido (MongoDB)

## 1. `docker-compose.yml` (Orquestación)

Este archivo define los 3 servicios que componen el sistema:

```yaml
services:
  mongo1:
    image: mongo:6
    container_name: mongo1
    ports:
      - "27017:27017" # Puerto local : Puerto contenedor
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin

  mongo2:
    image: mongo:6
    container_name: mongo2
    ports:
      - "27018:27017" # Puerto local (diferente)
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin

  storage_client:
    build:
      context: ./part2-distributed-storage
    depends_on:
      - mongo1
      - mongo2
```

mongo1 y mongo2: Son los dos "nodos" de nuestra base de datos distribuida. Son instancias idénticas de MongoDB. mongo1 se expone en el puerto 27017 del host y mongo2 en el 27018 para evitar conflictos.

storage_client: Es el contenedor que ejecuta nuestro script de Python (storage_system.py). Se construye usando el Dockerfile en esta carpeta.

depends_on: Asegura que el storage_client no intente iniciarse hasta que mongo1 y mongo2 estén listos.
