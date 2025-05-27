import structlog
from typing import Callable, Dict, Any

# Configurar el logger
logger = structlog.get_logger()

# Diccionario para registrar manejadores de eventos
event_handlers: Dict[str, Callable[[Any], None]] = {}

def register_event_handler(event_type: str, handler: Callable[[Any], None]) -> None:
    """Registrar un manejador para un tipo de evento específico."""
    event_handlers[event_type] = handler
    logger.info(f"Handler registrado para el tipo de evento: {event_type}")

def dispatch_event(event: Any) -> None:
    """Despachar un evento al manejador correspondiente."""
    event_type = event.tipo_evento
    handler = event_handlers.get(event_type)

    if handler:
        logger.info(f"Despachando evento de tipo {event_type} al manejador correspondiente.")
        handler(event)
    else:
        logger.warning(f"No se encontró manejador para el tipo de evento: {event_type}")