import pytest
from unittest.mock import MagicMock, patch
from src.application.event_handler import register_event_handler, dispatch_event, event_handlers

def test_register_event_handler():
    """Test que un handler se registra correctamente."""
    mock_handler = MagicMock()
    register_event_handler('test_event', mock_handler)
    assert 'test_event' in event_handlers
    assert event_handlers['test_event'] == mock_handler

def test_dispatch_event_with_handler():
    """Test que un evento se despacha al handler correcto."""
    mock_handler = MagicMock()
    mock_event = MagicMock()
    mock_event.tipo_evento = 'test_event'

    register_event_handler('test_event', mock_handler)
    dispatch_event(mock_event)
    mock_handler.assert_called_once_with(mock_event)

def test_dispatch_event_without_handler():
    """Test que se registra advertencia sin handler."""
    mock_event = MagicMock()
    mock_event.tipo_evento = 'unknown_event'

    with patch('src.application.event_handler.logger.warning') as mock_warning:
        dispatch_event(mock_event)
        mock_warning.assert_called_once_with('No se encontró manejador para el tipo de evento: unknown_event')