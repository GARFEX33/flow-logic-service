# Overview

`flow-logic-service` es un microservicio backend en Python que actúa como orquestador lógico de eventos dentro de un ecosistema basado en microservicios. Su función es recibir eventos desde un broker, ejecutar flujos definidos por tipo de evento, y coordinar la interacción con otros servicios. Esto facilita el desacoplamiento, la escalabilidad y la automatización.

# Core Features

* **Escucha de eventos del sistema**

  * Qué hace: Consume eventos desde Kafka.
  * Por qué importa: Permite reaccionar en tiempo real a acciones del usuario u otros servicios.
  * Cómo funciona: Usa `aiokafka` para suscribirse a tópicos y procesar eventos entrantes.

* **Orquestación de flujos**

  * Qué hace: Ejecuta secuencias lógicas según el evento recibido.
  * Por qué importa: Centraliza la lógica reactiva, permitiendo extensión y trazabilidad.
  * Cómo funciona: Registro dinámico de handlers, cada tipo de evento tiene su flujo.

* **Integración con servicios externos**

  * Qué hace: Invoca servicios como `image-processing-service` y `file-storage-service`.
  * Por qué importa: Composición de lógica reutilizando microservicios existentes.
  * Cómo funciona: HTTP/gRPC, según el servicio.

* **Reglas generales del motor de flujos**

  * Cada evento tiene un `tipo_evento` único.
  * Si no hay handler para un evento, se loguea como advertencia.
  * Estados posibles del flujo: `recibido`, `en_proceso`, `procesado`, `fallido`.
  * Los errores se registran junto con el detalle.

# User Experience

* **User personas**

  * Desarrollador backend: Quiere una arquitectura desacoplada y trazable.
  * Administrador de sistemas: Necesita monitorear la ejecución de eventos.

* **Key user flows**

  * Flujo de procesamiento de evento:

    1. Kafka emite un evento.
    2. Se identifica el `tipo_evento`.
    3. Se ejecuta el handler correspondiente.
    4. El handler invoca servicios externos.
    5. El resultado se registra en `flujo_ejecutado`.
    6. (Opcional) Se emite un nuevo evento.

* **UI/UX considerations**

  * No aplica: servicio sin interfaz de usuario.

# Technical Architecture

* **System components**: `flow-logic-service` (Python), Kafka, servicios HTTP externos, PostgreSQL (auditoría), Context7 MCP.

* **Data models**:

  ```python
  class Evento(BaseModel):
      id: UUID
      tipo_evento: str
      payload: dict
      timestamp: datetime

  class FlujoEjecutado(BaseModel):
      id: UUID
      tipo_evento: str
      payload: dict
      estado: Literal['recibido', 'en_proceso', 'procesado', 'fallido']
      timestamp: datetime
      error: Optional[str] = None
  ```

* **APIs and integrations**:

  * Kafka (broker): consumo con `aiokafka`
  * Servicios externos: HTTP/gRPC
  * Endpoint `/health`: exposición vía `FastAPI`
  * Context7 MCP: documentación activa de paquetes

* **Infrastructure requirements**:

  * Python 3.11+
  * Dockerizado
  * Kafka broker
  * PostgreSQL (opcional)
  * Variables de entorno via `.env`

* **Configuration**:

  ```env
  BROKER_URL=kafka://localhost:9092
  ENV=development
  SERVICE_NAME=flow-logic-service
  LOG_LEVEL=INFO
  AUDIT_DB_URL=postgresql://user:pass@host/db
  ```

* **File structure**:

  ```
  src/
  ├── application/         # Orquestación de flujos
  ├── domain/              # Tipos, interfaces, reglas de negocio
  ├── infrastructure/
  │   ├── messaging/       # Kafka consumer
  │   └── services/        # HTTP/gRPC a servicios externos
  ├── interfaces/
  │   ├── events/          # Suscriptores de eventos
  │   │   └── handlers/     # Handlers por tipo_evento
  │   └── http/            # Endpoint de healthcheck
  ├── config/              # Configuración y logger
  └── main.py              # Punto de entrada
  ```

# Development Roadmap

* **MVP requirements**:

  * Infraestructura base con Clean Architecture
  * Subscripción a Kafka
  * Validación de conexión con Kafka al iniciar el servicio
  * Logging estructurado
  * Registro de eventos en tabla `flujo_ejecutado`
  * Endpoint `/health`

* **Future enhancements**:

  * Emisión de nuevos eventos
  * Implementación de flujos complejos
  * Retry manager y circuit breaker
  * Trazabilidad distribuida (OpenTelemetry)

# Logical Dependency Chain

1. Estructura base del proyecto y configuración
2. Implementar consumer Kafka y verificar conexión inicial al broker
3. Registro dinámico de handlers
4. Manejador de flujo y transiciones de estado
5. Integración con servicios externos
6. Logging y persistencia

# Risks and Mitigations

* **Riesgo**: Falla en la conexión con Kafka

  * Mitigación: Pruebas con broker local y manejo de reconexiones + logs de conexión
* **Riesgo**: Servicios externos inestables

  * Mitigación: Retries + circuit breaker
* **Riesgo**: Falta de handlers registrados

  * Mitigación: Validación en startup + tests unitarios

# Testing Strategy

* Pruebas unitarias por handler
* Mock de servicios externos
* Validación de eventos con Pydantic
* Tests de integración por flujo completo
* Pruebas del cambio de estado del flujo

# Roles and Permissions (opcional)

* Acceso restringido vía token interno (no hay interfaz expuesta)

# Monitoring and Logging (opcional)

* Logs estructurados con `structlog`
* Métricas Prometheus opcionales
* Auditoría en PostgreSQL (opcional)

# Deployment Strategy (opcional)

* Docker + CI/CD
* Configuración por variables de entorno

# Maintenance Plan (opcional)

* Revisión mensual de flujos
* Actualización de dependencias por sprint

# Legal & Compliance (opcional)

* Cumplimiento de normativas internas y registro de logs

# Appendix

* **Research findings**:

  * Event-driven architecture
  * Orquestación vs coreografía
* **Technical specifications**:

  * Python 3.11+
  * aiokafka, pydantic, dependency-injector
  * structlog, FastAPI, Docker
