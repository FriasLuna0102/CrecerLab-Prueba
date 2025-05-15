# Wikipedia Analyzer

Wikipedia Analyzer es una aplicación web que permite buscar, analizar y guardar artículos de Wikipedia. La aplicación proporciona análisis detallados de los artículos, incluyendo conteo de palabras, palabras más frecuentes, análisis de sentimiento y reconocimiento de entidades.

![image](https://github.com/user-attachments/assets/aa632fc1-0969-4be1-9825-4de7f0115eeb)


---

## 🚀 Características Principales

- 🔍 **Búsqueda de artículos** en Wikipedia en tiempo real
- 📊 **Análisis de contenido**:
  - Conteo de palabras
  - Palabras más frecuentes (con visualización)
  - Análisis de sentimiento (positivo/negativo/neutral)
  - Reconocimiento de entidades (personas, lugares, organizaciones)
- 💾 **Guardado de artículos** para uso posterior
- 📝 **Notas personales** editables por cada artículo
- 📄 **Paginación** en la lista de artículos guardados
- 🌐 **Multilenguaje** (Español e Inglés) con i18next
- 📱 **Diseño responsivo** compatible con dispositivos móviles y de escritorio


## 🏗️ Arquitectura

El proyecto está dividido en tres capas principales:

1. **Frontend**: Aplicación en React con enrutamiento y traducciones
2. **Backend**: API REST en FastAPI que realiza el procesamiento del lenguaje natural
3. **Base de Datos**: PostgreSQL como motor de almacenamiento

### 📐 Decisiones de Diseño

- **Modularidad**: Código organizado por responsabilidad (API, servicios, modelos, etc.)
- **Patrón Repository**: Para desacoplar la lógica de acceso a datos
- **Servicios especializados**: NLP, sentimiento, entidades
- **Internacionalización centralizada**: i18next
- **Escalabilidad**: Pensado para crecimiento funcional

## 🧰 Tecnologías Utilizadas

### Frontend

- React 19
- React Router 7
- i18next
- Axios
- Vite
- CSS Modules

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- NLTK
- spaCy
- TextBlob

### Base de Datos

- PostgreSQL

---

## ⚙️ Instalación y Ejecución

### 🔧 Requisitos Previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker y Docker Compose (opcional)

---

### 🛠️ Configuración sin Docker

#### Backend (FastAPI)

1. **Clonar el repositorio**:

```bash
git clone https://github.com/tu-usuario/wikipedia-analyzer.git
cd wikipedia-analyzer
```

2. **Crear una base de datos PostgreSQL:**

```bash
sudo -u postgres psql
CREATE DATABASE wikipedia_analyzer;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE wikipedia_analyzer TO postgres;
\q
```

3.**Crear y activar un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
```

**4. Instalar dependencias:**

```bash
pip install -r requierements/base.txt
```

5. **Configurar variables de entorno:**
```bash

cp .env.example .env
```
# Editar .env con tus configuraciones

6. **Iniciar el servidor backend:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend (React)

Instalar dependencias:

```bash
cd frontend
npm install
```

Iniciar el servidor de desarrollo:

```bash
npm run dev
```

Abrir navegador en http://localhost:5173


# 🐳 Configuración con Docker

Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/wikipedia-analyzer.git
cd wikipedia-analyzer
```

Iniciar los contenedores con Docker Compose:
```bash
docker-compose up -d
```

## O ubicate en donde se encuentre el docker-compose y ejecuta:
```bash
docker-compose -f docker-compose.yml up --build
```

Abrir navegador en http://localhost:5173 para el frontend y http://localhost:8000/api/docs para la documentación de la API.

# 🧪 Ejecutar Pruebas
## El proyecto incluye pruebas unitarias e integración para el backend:
bashcd backend
pytest -v
🔌 Endpoints API
El backend expone los siguientes endpoints REST:
Búsqueda

GET /api/search/?q={query} - Busca artículos en Wikipedia

# Artículos

GET /api/articles/?skip={skip}&limit={limit} - Obtiene artículos guardados con paginación
GET /api/articles/detail/{page_id} - Obtiene detalles y análisis de un artículo
POST /api/articles/ - Guarda un artículo
PATCH /api/articles/{article_id} - Actualiza un artículo guardado (título, resumen o notas personales)
DELETE /api/articles/{article_id} - Elimina un artículo guardado

# 📁 Estructura del Proyecto
![image](https://github.com/user-attachments/assets/c75043aa-438a-4ec6-8a52-9571b7a9b165)

        
# 🧠 Justificación de la Arquitectura
## Backend
Tipado estático con Pydantic y generación automática de documentación OpenAPI. La estructura del proyecto sigue los principios de arquitectura limpia:

Controladores (API): Manejan las solicitudes HTTP y devuelven respuestas
Servicios: Contienen la lógica de negocio
Repositorios: Abstraen el acceso a datos
Schemas: Definen la validación y serialización de datos
Modelos: Representan las entidades de la base de datos

## Este enfoque permite:

Desacoplamiento: Cada capa puede evolucionar independientemente
Testabilidad: Facilita las pruebas unitarias y de integración
Mantenibilidad: Estructura clara y organizada

# Frontend
# La arquitectura del frontend se basa en componentes React con:

Componentes presentacionales y contenedores: Separación entre UI y lógica
Custom hooks: Para lógica reutilizable
Abstracción de servicios: Para comunicación con la API
Manejo de estado local: Con React Hooks (useState, useContext)
Internacionalización centralizada: Con i18next

# Esta estructura facilita:

Reutilización de código: Componentes modulares
Claridad conceptual: Separación de responsabilidades
Escalabilidad: Fácil adición de nuevas características

# 💡 Características de Desarrollo
## 📝 Análisis de Texto
análisis de texto implementa varias técnicas de procesamiento de lenguaje natural:

Frecuencia de palabras: Análisis estadístico de términos más usados
Análisis de sentimiento: Evaluación de la tonalidad emocional del texto (positivo/negativo/neutral)
Reconocimiento de entidades: Identificación de personas, organizaciones, lugares y otros elementos

# 📄 Paginación
La implementación de paginación utiliza el enfoque skip/limit para proporcionar una experiencia de usuario fluida al navegar por grandes colecciones de artículos guardados.
📝 Notas Personales
La funcionalidad de notas personales permite a los usuarios añadir y editar comentarios a los artículos guardados para uso personal.


# Imagenes de uso:
Desplegado:
![image](https://github.com/user-attachments/assets/82556eab-9a94-4e22-ab1b-4329814eae1f)

Prueba de backend:
![image](https://github.com/user-attachments/assets/8a203c47-93e4-41b7-9e68-68cc6c5e2170)

Busqueda:

![image](https://github.com/user-attachments/assets/c29275eb-15e1-4bca-b887-a57d810f40aa)

Detalle:

![image](https://github.com/user-attachments/assets/08ad9d7d-6c1c-4294-b0aa-5d2029f26a54)

Guardados:

![image](https://github.com/user-attachments/assets/2a89383e-c70e-4eb1-b77f-b032a4324749)

Dentro de los guardados:

![image](https://github.com/user-attachments/assets/bc7875f2-f623-4b75-9e59-1c9c85b4fd41)


