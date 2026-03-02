# Stefanini - challenge 1

[![Django](https://img.shields.io/badge/Django-6.0.2.x-092E20?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1.x-a30000)](https://www.django-rest-framework.org/)

> Api REST para la creación de tareas con colaboración.


## Pre- requisitos
- [Python](https://www.python.org/) >= 3.10
- [MySQL](https://www.mysql.com/) > 8.0.11 **or** [MariaDB](https://mariadb.org/) > 10.5
- [GROQ API Key](https://groq.com) for AI-powered assistant


## Decisiones técnicas

**`AbstractUser` sin modificaciones estructurales** — se extiende el modelo de usuario de Django agregando únicamente `unique=True` al campo email. Esto evita reimplementar autenticación, permisos y hashing de contraseñas desde cero.

**`username` se iguala al email al crear usuario** — dado que este proyecto no implementa un sistema de login, `username` se mantiene por compatibilidad interna con Django pero se establece igual al email para no requerir un campo adicional del cliente.

**Serializers desacoplados de los services** — los serializers validan la entrada y delegan la creación/modificación a `services.py`. Las vistas solo orquestan, nunca contienen lógica de negocio.

**`PATCH` en lugar de `PUT`** — los endpoints de actualización usan `PATCH` porque solo modifican campos específicos (estado o asignación), nunca la tarea completa.

**Respuestas JSON consistentes** — todos los endpoints siguen la misma estructura:
- Éxito: objeto o lista directamente
- Error: `{ "error": { "code": "...", "message": "..." } }`


## Validaciones

Django maneja internamente la validación de formato en campos como `EmailField`, por lo que no se reimplementa esa lógica en los serializers.

Las validaciones adicionales que sí se implementan son:

- **Email único** — a nivel de base de datos con `unique=True` y verificado en `services.py` antes de crear el usuario.
- **Título de tarea** — requerido, entre 3 y 120 caracteres.
- **Descripción** — opcional, máximo 500 caracteres.
- **Estado** — solo acepta valores del enum: `TODO`, `IN_PROGRESS`, `DONE`.
- **Usuario asignado** — si se envía un `assigned_to_id`, se verifica que el usuario exista antes de crear o modificar la tarea.


## Flujo de estados

Las transiciones de estado están controladas y no todas son permitidas:

```
TODO → IN_PROGRESS → DONE
```



## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-proyecto>.git
   cd stefanini-challenge
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # Unix/macOS
   source .venv/bin/activate
   ```
3. Instalar dependencias:
   pip install --upgrade pip
> [!NOTE]
> este repositorio utiliza `uv` y genera el archivo `uv.lock`.
> - se recomienda emplear `uv` en lugar de `pip` cuando esté disponible:
> - uv install

   si no dispones de uv, el siguiente comando clásico sigue funcionando:
   pip install -r requirements.txt   # o `pip install .` según el gestor

4. Configurar la base de datos en `settings/settings.py` (MySQL/MariaDB).
5. Ejecutar migraciones y crear un superusuario:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
7. Acceder a la API en `http://localhost:8000/` y al panel de admin por defecto.

## Documentación de la API

La API se documenta automáticamente usando **drf-spectacular**. Una vez el
servidor esté en funcionamiento, es posible:

- Obtener el esquema OpenAPI/JSON en `GET /api/schema/`.
- Navegar la interfaz Swagger UI en `GET /api/docs/`.

Los endpoints disponibles (usuarios y tareas) se describen con sus parámetros,
modelos de request/response y ejemplos. La configuración se encuentra en
`settings/settings.py`, y el esquema se genera a partir de los viewsets/funciones
registrados en `urls.py`.

## Alex

El proyecto integra **Alex**, un asistente inteligente impulsado por [Groq](https://groq.com) y el modelo `llama-3.3-70b-versatile`, capaz de responder preguntas sobre el sistema, los usuarios y sus tareas asignadas.

> [!NOTE]
> Para usar el asistente necesitas una `GROQ_API_KEY` válida configurada en tu archivo `.env`.
> Puedes obtener una gratis en [https://console.groq.com/keys](https://console.groq.com).

### Endpoint
```
POST /api/v1/assistant/consult/
```

### Body
```json
{
    "pregunta": "¿Quién soy y qué tareas tengo?",
    "session_id": "sesion-1",
    "user_id": 2
}
```

> [!IMPORTANT]
> El `session_id` es clave para el historial de conversación. Usa el mismo identificador en todas las preguntas de una misma sesión. Si cambias el `session_id`, la conversación empieza desde cero.

> [!WARNING]
> El historial se almacena en memoria RAM del servidor. Si el servidor se reinicia, las sesiones se pierden. Esto es intencional porque no se definio en la BD.

### Response
```json
{
    "pregunta": "¿Quién soy, qué tareas tengo y que pregunte anteriormente?",
    "respuesta": "Eres Johann..."
}
```

## Arquitectura

El proyecto sigue la arquitectura **MVT** (Model‑View‑Template) nativa de Django.
Cada aplicación (`user`, `tasks`) mantiene la misma estructura mínima:

- `models.py` – definición de datos.
- `services.py` – lógica de negocio y validaciones adicionales.
- `serializer.py` – transformación entre objetos Python y JSON.
- `views.py` – puntos finales REST usando `@api_view`.
- `urls.py` – rutas específicas de la app.

La carpeta `settings/` contiene la configuración global y las rutas principales.
Django maneja internamente, por ejemplo, la validación de campos (`EmailField`,
longitudes, etc.), por lo que las aplicaciones sólo añaden reglas de negocio
específicas (como el email único o las transiciones de estado).

**Tasks** y **Users** comparten el mismo patrón; esto facilita el escalado y
la incorporación de nuevas funcionalidades, ya que el desarrollador siempre
sabe dónde ubicar cada tipo de código.
