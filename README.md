 Mascotas Perdidas 

 

 Aplicación web para reportar y encontrar mascotas perdidas. Incluye

 reconocimiento de imágenes para sugerir posibles coincidencias entre

 mascotas reportadas como perdidas y encontradas, y un mapa con los

 avisos activos.

 

 Este proyecto es un ejercicio de aprendizaje end to end: parte desde

 un CRUD básico hasta un sistema de coincidencias basado en un modelo

 de inteligencia artificial preentrenado (CLIP).

 

  Funcionalidades actuales

 

 \- Crear y consultar reportes de mascotas perdidas o encontradas.

 \- Mapa interactivo (Leaflet) con los reportes activos, con búsqueda

  por radio de cercanía.

 \- Creación de reportes directamente desde el mapa, incluyendo la

  subida de una foto real.

 \- Reconocimiento de imágenes: cada foto se convierte en un vector

  numérico (embedding) mediante el modelo CLIP, y el sistema sugiere

  posibles coincidencias entre reportes de tipo opuesto (perdida ↔

  encontrada) según:

  - Similitud visual entre las fotos.

  - Similitud semántica entre las descripciones escritas.

  - Filtro por especie, para evitar comparaciones sin sentido.

 

  Stack técnico

 

 \- \*\*Backend:\*\* FastAPI (Python)

 \- \*\*Base de datos:\*\* PostgreSQL, con la extensión PostGIS para

  almacenar y consultar ubicaciones geográficas

 \- \*\*Reconocimiento de imágenes:\*\* CLIP, mediante la librería

  `sentence-transformers`

 \- \*\*Frontend:\*\* plantillas HTML con Jinja2, JavaScript simple y

  Leaflet.js para el mapa

 \- \*\*Entorno:\*\* Python ejecutado localmente con un entorno virtual

  (`venv`); no se utiliza Docker en la configuración actual

 

  Requisitos previos

 

 \- Python 3.13 instalado, con la opción "Add python.exe to PATH"

  marcada durante la instalación

 \- PostgreSQL instalado localmente, con la extensión PostGIS habilitada

 \- Git

 

  Instalación y ejecución local

 

    1\. Clonar el repositorio y ubicarse en la carpeta del proyecto.

    

    2\. Crear la base de datos en PostgreSQL (por ejemplo, desde pgAdmin)

    y habilitar la extensión PostGIS en ella:

    ```sql

    CREATE EXTENSION postgis;

    ```

    

    3\. Copiar el archivo de variables de entorno de ejemplo y completar

    los datos de conexión reales:

    

    

    copy .env.example .env

    

    El formato esperado es:

    

    DATABASE\_URL=postgresql+psycopg2://usuario:contraseña@localhost:puerto/nombre\_basededatos

    

    

    4\. Crear el entorno virtual e instalar las dependencias:

    

    python -m venv venv

    venv\\Scripts\\activate

    pip install -r requirements.txt

    

    

    5\. Ejecutar el servidor:

    

    python -m uvicorn app.main:app

    

    

    6\. Abrir en el navegador:

    - `http://127.0.0.1:8000/docs` — documentación interactiva de la API

    - `http://127.0.0.1:8000/mapa` — mapa de reportes

 

  Estructura del proyecto

 

 mascotas-perdidas/

 ├── app/

 │ ├── init.py

 │ ├── main.py # Punto de entrada de la aplicación

 │ ├── database.py # Configuración de la conexión a la base de datos

 │ ├── models.py # Modelos de la base de datos

 │ ├── schemas.py # Esquemas de entrada y salida de la API

 │ ├── ai.py # Carga del modelo CLIP y cálculo de embeddings

 │ ├── routers/

 │ │ ├── init.py

 │ │ └── reportes.py # Endpoints de la API

 │ ├── templates/

 │ │ └── mapa.html # Página del mapa

 │ └── static/

 │ └── uploads/ # Fotos subidas por los usuarios

 ├── probar\_embeddings.py # Script de prueba aislado para CLIP

 ├── requirements.txt

 ├── .env.example

 ├── .gitignore

 └── README.md

 

 

  Fases del proyecto

 

 # Completadas

 

 1\. \*\*CRUD básico\*\* — creación y consulta de reportes, conectados a

   PostgreSQL mediante SQLAlchemy.

 2\. \*\*Mapa y geolocalización\*\* — visualización de reportes en un mapa

   interactivo, con búsqueda por radio usando PostGIS.

 3\. \*\*Subida de imágenes\*\* — carga de fotos reales asociadas a cada

   reporte, servidas como archivos estáticos.

 4\. \*\*Reconocimiento de imágenes\*\* — cálculo de embeddings con CLIP,

   comparación por similitud de coseno entre imágenes y

   descripciones, con filtro por especie.

 

 # Próximas fases (hoja de ruta)

 

 5\. \*\*Usuarios y autenticación\*\* — registro e inicio de sesión,

   vista de reportes propios y sus coincidencias, y contacto mediado

   por la plataforma entre las personas involucradas en un posible

   match, para proteger su información de contacto.

 6\. \*\*Adopciones\*\* — un tercer tipo de reporte para animales en busca

   de hogar, con filtros por tipo de reporte y un proceso de

   postulación para quienes deseen adoptar.

 7\. \*\*Despliegue\*\* — publicación del proyecto en un servicio en la

   nube, para que sea accesible sin depender de un entorno local.

 8\. \*\*Capa analítica con dbt\*\* — modelado de los datos del proyecto

   con dbt sobre PostgreSQL, para generar métricas de uso (reportes

   por zona, tasa de coincidencias, tiempos de resolución) y

   conectarlas a una herramienta de visualización.

 

 Estas fases futuras se desarrollarán en ramas separadas del

 repositorio, como parte del aprendizaje de control de versiones con

 Git.

