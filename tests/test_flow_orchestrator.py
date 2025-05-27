"""Tests for the flow orchestrator."""

import pytest
from unittest.mock import patch, MagicMock
from src.application.flow_orchestrator import orchestrate_flow

@pytest.mark.asyncio
async def test_orchestrate_flow_success():
    """Test successful flow orchestration."""
    event = {
        "id": "test_id",
        "data": {"key": "value"}
    }

    with patch("src.application.flow_orchestrator.db") as mock_db:
        mock_db.save_flujo_ejecutado = MagicMock(return_value="test_id")
        mock_db.update_flujo_ejecutado = MagicMock(return_value=None)

        await orchestrate_flow(event)

        assert mock_db.save_flujo_ejecutado.called_once()
        assert mock_db.update_flujo_ejecutado.call_count == 2
        assert mock_db.update_flujo_ejecutado.call_args_list[1][0][0]["status"] == "procesado"

@pytest.mark.asyncio
async def test_orchestrate_flow_failure():
    """Test flow orchestration with an exception."""
    event = {
        "id": "test_id",
        "data": {"key": "value"}
    }

    with patch("src.application.flow_orchestrator.db") as mock_db:
        mock_db.save_flujo_ejecutado = MagicMock(return_value="test_id")
        mock_db.update_flujo_ejecutado = MagicMock(return_value=None)
        with patch("src.application.flow_orchestrator.asyncio.sleep", side_effect=Exception("Test error")):
            await orchestrate_flow(event)

            assert mock_db.save_flujo_ejecutado.called_once()
            assert mock_db.update_flujo_ejecutado.call_count == 2
            assert mock_db.update_flujo_ejecutado.call_args_list[1][0][0]["status"] == "fallido"
            assert "error" in mock_db.update_flujo_ejecutado.call_args_list[1][0][0]["data"]