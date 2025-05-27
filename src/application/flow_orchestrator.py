"""Flow Orchestration and State Management."""

import asyncio
import logging
from typing import Any, Dict
from src.infrastructure.persistence.database import db
from src.infrastructure.persistence.models import FlujoEjecutado

logger = logging.getLogger(__name__)

async def orchestrate_flow(event: Dict[str, Any]) -> None:
    """Orchestrate the flow execution and manage state transitions."""
    flujo_id = event.get("id")
    flujo_data = event.get("data")

    # Create FlujoEjecutado record with initial state
    flujo = FlujoEjecutado(id=flujo_id, data=flujo_data, status="recibido")
    flujo_id = db.save_flujo_ejecutado(flujo.model_dump())

    try:
        # Update state to en_proceso
        flujo.status = "en_proceso"
        await db.update_flujo_ejecutado(flujo.model_dump())

        # Execute event handler (simulated here)
        await asyncio.sleep(1)  # Simulate handler execution
        logger.info(f"Processed event {flujo_id}")

        # Update state to procesado
        flujo.status = "procesado"
    except Exception as e:
        # Handle exceptions and update state to fallido
        flujo.status = "fallido"
        flujo.data["error"] = str(e)
        logger.error(f"Error processing event {flujo_id}: {e}")
    finally:
        # Persist final state
        await db.update_flujo_ejecutado(flujo.model_dump())