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

    logger.info(f"Starting orchestration for event: {flujo_id}")

    # Create FlujoEjecutado record with initial state
    flujo = FlujoEjecutado(id=flujo_id, data=flujo_data, status="recibido")
    saved_id = db.save_flujo_ejecutado(flujo.model_dump())
    logger.info(f"Saved flujo with ID: {saved_id}")

    try:
        # Update state to en_proceso
        flujo.status = "en_proceso"
        await db.update_flujo_ejecutado(flujo.model_dump())
        logger.info(f"Updated flujo status to en_proceso")

        # Execute event handler (simulated here)
        await asyncio.sleep(1)  # Simulate handler execution
        logger.info(f"Processed event {flujo_id}")

        # Update state to procesado
        flujo.status = "procesado"
        logger.info(f"Updating flujo status to procesado")
    except Exception as e:
        # Handle exceptions and update state to fallido
        flujo.status = "fallido"
        flujo.data["error"] = str(e)
        logger.error(f"Error processing event {flujo_id}: {e}")
    finally:
        # Persist final state
        logger.info(f"Final update for flujo {flujo_id} with status {flujo.status}")
        await db.update_flujo_ejecutado(flujo.model_dump())
        logger.info(f"Final state persisted for flujo {flujo_id}")