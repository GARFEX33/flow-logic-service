# Overview

`flow-logic-service` es un microservicio backend que actúa como orquestador lógico de eventos en el ecosistema de aplicaciones. Su objetivo es escuchar eventos emitidos por otros servicios y ejecutar flujos definidos en función del tipo de evento. Este servicio es clave para lograr desacoplamiento, escalabilidad y automatización en la arquitectura basada en microservicios.

# Core Features

* **Escucha de eventos del sistema**

  * Qué hace: Consume eventos desde un broker de eventos.
  * Por qué importa: Permite reaccionar en tiempo real a acciones del usuario u otros servicios.
  * Cómo funciona: Suscripción a tópicos configurados en un broker (Kafka, NATS, etc.) y disparo de handlers.

* **Orquestación de flujos**

  * Qué hace: Ejecuta acciones coordinadas según el evento recibido.
  * Por qué importa: Centraliza la lógica de negocio reactiva, facilitando extensibilidad y trazabilidad.
  * Cómo funciona: Cada tipo de evento activa un handler específico que puede disparar llamadas a otros servicios, guardar datos o emitir nuevos eventos.

* **Integración con servicios externos**

  * Qué hace: Se comunica con servicios como `image-processing-service` y `file-storage-service`.
  * Por qué importa: Permite componer lógica de negocio reutilizando microservicios existentes.
  * Cómo funciona: Uso de HTTP/gRPC/cola de mensajes según el tipo de integración.

* **Reglas generales del motor de flujos**

  * Cada evento debe tener un tipo único (`tipo_evento`) que lo identifique.
  * Para cada tipo, debe registrarse un handler (uso de registro dinámico o diccionario de funciones).
  * Si no hay handler para un evento, este se descarta con log de advertencia.
  * Los errores deben capturarse y marcar el flujo como `fallido`, con detalle del error.
  * Un flujo puede estar en estado: `recibido`,`en_proceso` `procesado`, `fallido`.

# User Experience

* **User personas**

  * Desarrollador backend: Quiere una arquitectura clara y desacoplada para manejar eventos del sistema.
  * Administrador de sistemas: Requiere trazabilidad y monitoreo de los eventos procesados.

* **Key user flows**

  * Plantilla de flujo para eventos (base para futuros flujos):

    1. Recepción del evento desde Kafka.
    2. Identificación del tipo de evento.
    3. Ejecución del handler registrado para ese tipo.
    4. Handler orquesta acciones necesarias (invocaciones a servicios, transformaciones, almacenamiento).
    5. Resultado registrado en la tabla `flujo_ejecutado`.
    6. (Opcional) Emisión de nuevos eventos.

* **UI/UX considerations**

  * No aplica: servicio backend sin interfaz de usuario.

# Technical Architecture

* **System components**: flujo-logico-service (backend), broker de eventos, servicios externos (file-storage, image-processing), logging o base mínima para trazabilidad.

* **Data models**:

  * Evento (tipo, payload, timestamp, id)
  * flujo\_ejecutado:

    ```json
    {
      "id": "uuid",
      "tipo_evento": "string",
      "payload": {},
      "estado": "recibido | en_proceso| procesado | fallido",
      "timestamp": "datetime",
      "error": "string (opcional)"
    }
    ```

* **APIs and integrations**:

  * Kafka como broker de eventos
  * HTTP o gRPC para comunicarse con servicios externos
  * Logs estructurados para trazabilidad (con opción a PostgreSQL si se requiere almacenamiento de auditoría)

* **Infrastructure requirements**:

  * Dockerized service
  * Conexión con broker Kafka
  * (Opcional) Base Postgres compartida o local para auditoría mínima
  * Healthcheck endpoint (`/health`) para readiness

* **Configuration**:

  * Variables de entorno esperadas:

    * `BROKER_URL`
    * `ENV`
    * `SERVICE_NAME`
    * `LOG_LEVEL`
    * `AUDIT_DB_URL` (opcional)

  * Carga mediante `dotenv` o similar

* **File structure**:

  ```
  src/
  ├── application/         # Casos de uso: lógica de orquestación
  ├── domain/              # Tipos, interfaces, reglas de negocio puras
  ├── infrastructure/
  │   ├── messaging/       # Kafka setup
  │   └── services/        # HTTP/gRPC hacia servicios externos
  ├── interfaces/
  │   ├── events/          # Suscriptores (event listeners)
  │   │   └── handlers/     # Handlers por tipo de evento
  │   └── http/            # Healthcheck endpoint
  ├── config/              # Envs, logger, constantes globales
  └── main.ts              # Entry point del servicio
  ```

# Development Roadmap

* **MVP requirements**:

  * Infraestructura base (Clean Architecture, conexión eventos)
  * Logging estructurado o guardado en tabla `flujo_ejecutado`
  * Endpoint `/health` para monitoreo

* **Future enhancements**:

  * Definición e implementación de flujos específicos por tipo de evento
  * Emisión de nuevos eventos según reglas de negocio
  * Logs estructurados y trazabilidad distribuida

# Logical Dependency Chain

1. Configuración del entorno y arquitectura base
2. Subscripción a eventos desde Kafka
3. Diseño modular para handlers de flujos (sin implementación aún)
4. Validación de eventos con Zod
5. Registro de handlers dinámico
6. Implementación de `FlujoOrchestrator`
7. Mecanismo de transición de estados de flujo
8. Implementación de `RetryManager` y manejo de errores

# Risks and Mitigations

* **Riesgo**: Dificultad en integración con broker de eventos

  * Mitigación: Pruebas locales con broker simulado antes del despliegue

* **Riesgo**: Fallos en servicios externos

  * Mitigación: Retries y circuit breakers en llamadas a servicios

* **Riesgo**: Handlers mal registrados o ausentes

  * Mitigación: Validación al levantar el servicio, log de advertencia y test unitarios de cobertura

# Testing Strategy

* Pruebas unitarias en servicios backend
* Validaciones del esquema de eventos
* Mock de servicios externos para pruebas de orquestación
* Pruebas de integración para orquestación completa de eventos
* Criterios de aceptación definidos por tipo de evento (cuando existan)
* Pruebas de flujo completo con estados

# Roles and Permissions (opcional)

* Solo accesible por otros servicios autenticados mediante token interno. No expone interfaz pública.

# Monitoring and Logging (opcional)

* Logs estructurados por tipo de evento (Pino recomendado)
* Métricas Prometheus opcionales: `eventos_total`, `eventos_fallidos`, `eventos_por_tipo`
* Registro de trazabilidad en base de datos opcional

# Deployment Strategy (opcional)

* Docker + CI/CD para despliegue automático
* Configuración vía variables de entorno

# Maintenance Plan (opcional)

* Revisión mensual de flujos activos
* Actualización de dependencias cada sprint

# Legal & Compliance (opcional)

* Cumplimiento con políticas internas de manejo de datos y logs

# Appendix

* **Research findings**:

  * Event-driven design patterns
  * Orquestación vs coreografía

* **Technical specifications**:

  * Node.js + TypeScript
  * kafkaJS (event broker)
  * zod (validación)
  * tsyringe (inyección dependencias)
  * Dockerizado, sin UI, sin lógica de negocio persistente
  * Todas las tecnologías y librerías listadas están confirmadas como parte del stack base y se espera su uso por defecto.
  * La documentación del código debe seguir las convenciones establecidas por `contex7`, incluyendo uso de anotaciones MCP (`Context7 MCP`) para mantener sincronización entre especificaciones y comportamiento del código fuente. Esta práctica es obligatoria para cualquier solicitud o módulo implementado.
