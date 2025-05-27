"""Tests for the persistence layer."""

import pytest
from unittest.mock import patch
from src.infrastructure.persistence.database import db

@pytest.mark.asyncio
async def test_save_flujo_ejecutado():
    """Test saving a FlujoEjecutado record."""
    flujo = {
        "id": "test_id",
        "data": {"key": "value"},
        "status": "active"
    }

    with patch.object(db, "execute", return_value="test_id") as mock_execute:
        result = await db.save_flujo_ejecutado(flujo)
        assert result == "test_id"
        mock_execute.assert_called_once()

@pytest.mark.asyncio
async def test_update_flujo_ejecutado():
    """Test updating a FlujoEjecutado record."""
    flujo = {
        "id": "test_id",
        "data": {"key": "value"},
        "status": "inactive"
    }

    with patch.object(db, "execute") as mock_execute:
        await db.update_flujo_ejecutado(flujo)
        mock_execute.assert_called_once()